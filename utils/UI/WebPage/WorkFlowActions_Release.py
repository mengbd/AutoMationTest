import json
import os
import time
import re
import random
import logging

from selenium.webdriver import ActionChains
from config.globalVars import UIGlobalVars
from utils.UI.WebPage.BasePage import WebPage
from utils.UI.read_element import Element
from utils.Others.OSOperation import list_folder
from ..read_element import read_config

from pykeyboard import PyKeyboard
from pymouse import PyMouse
import pyperclip
from Models.z_workflow import IFlowInstance
from utils.DBConnect.Oracle import DataBaseOperation
from config.globalVars import DataBaseGlobalVars
from collections import Iterable

log = logging.getLogger(__file__)
G = UIGlobalVars()


class LoginPlatform(object):
    """
    登录操作基类
    """

    def __init__(self, driver):
        self.driver = driver
        self.ip = G.Server_IP
        self.port = G.Server_Port
        self.basePage = WebPage(driver=self.driver)
        self.LoginURL = "http://" + self.ip + ":" + str(self.port) + "/z_user_org_right/Login/index"
        self.UserLoginData = self.LoadUserConfig()
        self.CreateWorkFlowUser = None
        self.WorkFlowDetailConfig = None
        self.IndexMenuConfig = None

    def login(self, login_user="管理员"):
        """
        需要登录操作的通用方法
        :param login_user:需要登录的人名，账号密码存放于/resource/PlatformUsers/PlatFormUsers.json中
        :return:
        """
        log.info("读取%s的账号密码信息" % login_user)
        username, password = eval(self.UserLoginData[login_user])
        log.info("读取登录页元素定位配置")
        setattr(self, 'LoginConfig', read_config('z_user_org_rightLoginindex'))
        log.info("开始打开页面")
        self.basePage.get_url(self.LoginURL)
        log.info("输入登录名")
        self.basePage.input_text(self.LoginConfig["userName"], username)
        log.info("输入密码")
        self.basePage.input_text(self.LoginConfig["userPwd"], password)
        log.info("点击登录跳转")
        self.basePage.is_click(self.LoginConfig["btnLogin"])
        self.CreateWorkFlowUser = login_user

    def LoadUserConfig(self):
        UserConfigJson = os.path.join(os.path.join(G.resource_path, "PlatFormUsers"), "PlatformUsers.json")
        with open(UserConfigJson, 'r', encoding='utf-8') as f:
            UserLoginData = f.read()
            return json.loads(UserLoginData)


class WorkFlowActions(LoginPlatform):

    def __init__(self, driver):
        self.instance_id = None
        super().__init__(driver)

    def get_this_instance_id(self):
        this_url = self.basePage.url()
        assert this_url
        url = re.search(r'flowInstanceId=(?P<id>.{32})', this_url)
        assert url
        return url.group('id')

    def create_work_flow(self, menu_name="系统流程", tag_name="督办"):
        """
        创建指定的流程，需要提前在web上配置
        :param menu_name: 左侧的流程目录名
        :param tag_name: 选中流程目录名后具体的流程tag名
        :return:
        """
        self.IndexMenuConfig = read_config("z_web_containerHomeblueIndex")
        log.info("点击新建流程按钮")
        self.basePage.is_click(self.IndexMenuConfig["新建流程"])
        log.info("切换iframe至新建流程")
        self.basePage.switch(self.IndexMenuConfig["切换iframe"])
        log.info("查找新建办件标签")
        clicks = self.basePage.find_elements(("css", 'label'))
        for menu in clicks:
            if menu.text == menu_name:
                log.info("找到%s菜单" % menu)
                menu.click()
        log.info("寻找%s按钮" % tag_name)
        workflows = self.basePage.find_elements(('css', '.modal-body-tag'))
        for flow_btn in workflows:
            if tag_name in flow_btn.text:
                flow_btn.find_element_by_css_selector(
                    ".process-add").click()

    def change_to_workflow(self, send_user="管理员", *args, **kwargs):

        """
        创建指定流程后转件给指定人
        :param send_user: 转件给名字为所赋值的人，如果出现多次，则都会被选中
        :return:
        """
        flow_status = kwargs.get('flow_status')
        options = kwargs.get('options')
        is_child = kwargs.get('is_child')
        self.switch_to_the_last_window()
        # 转件选择人配置
        self.WorkFlowDetailConfig = Element("work_flow_details")
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        self.basePage.is_click(self.WorkFlowDetailConfig["转件按钮"])
        if options:
            self.insert_options()

        # 创建完成后会自动进入下一环节，登录所转件人账号进行校验，校验方式为切换至iframe中找寻创建件时的实例ID 的td标签
        if not flow_status:
            nodes = self.basePage.find_elements(self.WorkFlowDetailConfig["转件人"])
            for i in nodes:
                if i.text == send_user:
                    i.click()
            self.basePage.is_click(self.WorkFlowDetailConfig["确定转件"])
            if is_child:
                self.reverse_instance_id()
            self.check_flow_create_or_false(login_user=send_user)
        else:
            if kwargs.get("auto") is True:
                nodes = self.basePage.find_elements(self.WorkFlowDetailConfig["转件人"])
                for i in nodes:
                    if i.text == send_user:
                        i.click()
                self.basePage.is_click(self.WorkFlowDetailConfig["确定转件"])
                if is_child:
                    self.reverse_instance_id()
            self.check_flow_create_or_false(login_user=send_user, flow_status=flow_status)

    def change_to_workflow_with_same_level(self, send_user="管理员", *args, **kwargs):
        flow_status = kwargs.get('flow_status')
        options = kwargs.get('options')
        self.switch_to_the_last_window()
        # 转件选择人配置
        self.WorkFlowDetailConfig = Element("work_flow_details")
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        self.basePage.is_click(self.WorkFlowDetailConfig["同级转件"])
        if options:
            self.insert_options()

        # 创建完成后会自动进入下一环节，登录所转件人账号进行校验，校验方式为切换至iframe中找寻创建件时的实例ID 的td标签
        if not flow_status:
            nodes = self.basePage.find_elements(self.WorkFlowDetailConfig["转件人"])
            for i in nodes:
                if i.text == send_user:
                    i.click()

            self.basePage.is_click(self.WorkFlowDetailConfig["确定转件"])
            self.check_flow_create_or_false(login_user=send_user)
        else:
            self.check_flow_create_or_false(login_user=send_user, flow_status=flow_status)

    def reverse_instance_id(self):
        """
        父流程创建子流程时使用,
        """
        if not hasattr(self, 'parent_flow_id'):
            databaseconfig = DataBaseGlobalVars()
            connection_data = databaseconfig.data_base_config
            connect_data = {'Z_WORKFLOW': connection_data['Z_WORKFLOW']}
            DBsession = DataBaseOperation(connect_data)
            dbsession = DBsession.session
            child_flow = dbsession.query(IFlowInstance.id).filter(
                IFlowInstance.parent_flow_ins_id == self.instance_id).all()
            if child_flow:
                setattr(self, 'parent_flow_id', self.instance_id)
                self.instance_id = child_flow[0].id
            else:
                raise AttributeError("Can not found Child Flow")
        else:
            assert hasattr(self, 'parent_flow_id')
            self.instance_id, self.parent_flow_id = self.parent_flow_id, self.instance_id

    def change_to_workflow_multiple(self, send_user=tuple("管理员"), *args, **kwargs):

        """
        对于多个转件人的补充，只转件，不提供检查件是否转送成功(多个收件人无法确定使用哪个确认件)
        :param send_user: 转件给名字为所赋值的人，如果出现多次，则都会被选中
        :return:

        """

        assert isinstance(send_user, Iterable)
        options = kwargs.get('options')
        is_child = kwargs.get('is_child')
        self.switch_to_the_last_window()
        # 转件选择人配置
        self.WorkFlowDetailConfig = Element("work_flow_details")
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        self.basePage.is_click(self.WorkFlowDetailConfig["转件按钮"])
        if options:
            self.insert_options()
        nodes = self.basePage.find_elements(self.WorkFlowDetailConfig["转件人"])
        for i in nodes:
            if i.text in send_user:
                i.click()
        self.basePage.is_click(self.WorkFlowDetailConfig["确定转件"])
        if is_child:
            self.reverse_instance_id()

    def check_flow_create_or_false(self, login_user="管理员", flow_status="待办"):
        """
        校验之前存在的工作流是否存在，如果存在会进入该工作流
        :param instance_id: 工作流实例ID，创建件时解析URL所得
        :param login_user: 本次登录名，如果与前一环节创建人不同，则会重新登录
        :return:
        """
        log.info("切换至首页")
        self.switch_to_the_first_window()
        log.info("切换出iframe")
        self.driver.switch_to.default_content()
        if self.CreateWorkFlowUser == login_user:

            # 创建人与转件人相同
            log.info("点击首页按钮")
            self.basePage.is_click(self.IndexMenuConfig["首页按钮"])
            self.close_all_pages()
            log.info("点击办件中心")
            self.basePage.is_click(self.IndexMenuConfig["办件中心"])

            log.info("切换至办件中心iframe")
            self.basePage.switch(("xpath", "/html/body/div/div[2]/iframe"))
        else:
            now_user = self.UserLoginData[login_user]
            if not now_user:
                raise AttributeError("User Mapping Has not Found That User %s" % login_user)

            self.basePage.is_click(self.IndexMenuConfig["用户注销"])
            self.login(login_user)
            log.info("点击办件中心")
            self.basePage.is_click(self.IndexMenuConfig["办件中心"])

            log.info("切换至办件中心iframe")
            self.basePage.switch(("xpath", "/html/body/div/div[2]/iframe"))
        time.sleep(5)
        btns = self.basePage.find_elements(self.IndexMenuConfig["办件中心状态按钮"])
        for i in btns:
            if flow_status in i.text:
                i.click()
        workflow_btn = None
        instance = self.basePage.find_element(('css', "td[title='%s']" % self.instance_id))
        # 办件中心的件下每个件下有一个td 标签，title属性为创建工作流失的flowinstance_id
        assert instance != []
        time.sleep(3)
        workflow_btn = self.basePage.find_elements(('css', "td[title='%s'] + td + td" % self.instance_id))
        index = 0
        if len(workflow_btn) > 1:
            index = -1
        setattr(self, 'bussiness_number', workflow_btn[index].text)
        if flow_status == "待办":
            if index == 0:
                status_btn = self.basePage.find_element(('css', "td[title='%s'] + td + td + td" % self.instance_id))
                setattr(self, 'link_status', status_btn.text)
                flow_name = self.basePage.find_element(
                    ('css', "td[title='%s'] + td + td + td + td + td" % self.instance_id))
                setattr(self, 'flow_name', flow_name.text)
                node_name = self.basePage.find_element(
                    ('css', "td[title='%s'] + td + td + td + td + td + td" % self.instance_id))
                setattr(self, 'node_name', node_name.text)
                node_left_time = self.basePage.find_element(
                    ('css', "td[title='%s'] + td + td + td + td + td + td + td" % self.instance_id))
                flow_left_time = self.basePage.find_element(
                    ('css', "td[title='%s'] + td + td + td + td + td + td + td + td" % self.instance_id))
                setattr(self, 'node_left_time', node_left_time.text)
                setattr(self, 'flow_left_time', flow_left_time.text)
        ActionChains(self.driver).move_by_offset(0, 170)

        ActionChains(self.driver).move_to_element(workflow_btn[index]).double_click(workflow_btn[index]).perform()

    def close_all_pages(self):
        script = """for (var i=0;i<$(".tabbar-item-close").length;i ++ ){
                        $(".tabbar-item-close")[i].click()
                        }"""
        self.basePage.driver.execute_script(script)

    def return_message(self, login_user="管理员", index=0):
        """

        :param login_user: 退件给xx。默认为管理员
        :param index: 环节按钮/暂时采用这个方式，退件选择退到某环节时，按钮的顺序，从左到右为，0，1，2...，倒数采用-1， -2
        :return:
        """
        self.switch_to_the_last_window()
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        # 转件选择人配置
        self.basePage.is_click(self.WorkFlowDetailConfig["退回"])
        nodes = self.basePage.find_elements(self.WorkFlowDetailConfig["退回节点"])
        log.info("一共找到%s个退回节点，" % len(nodes))
        nodes[index].click()
        self.basePage.input_text(self.WorkFlowDetailConfig["退回原因"], "This is A Test Message")
        self.basePage.is_click(self.WorkFlowDetailConfig["确定退回"])
        # self.basePage.is_click(detail_config["弹框确认"])
        self.click_second_pop(action=0)
        ## 二层嵌套弹框selenium无法识别，改为使用Selenium执行JQuery语句完成确认退回
        # submit = self.basePage.driver.find_element_by_css_selector("span[index=0]")
        # submit.click()
        self.check_flow_create_or_false(login_user=login_user)

    def check_users(self, exclude):

        """
        校验工作流详情页左侧流程明细中的环节是否一致
        :param exclude: 需要排除的人, Array > ["管理员", "王宝峰" ]
        :return:
        """
        self.switch_to_the_last_window()
        users = self.basePage.find_elements(self.WorkFlowDetailConfig["流程办理用户"])
        assert type(exclude) is list
        log.info("当前流程一共%s个流程明细" % len(users))
        for i in exclude:
            for j in users:
                assert i not in j.text

    def drop_workflow(self, apply_to='管理员'):
        """
        作废工作流环节
        :return:
        """
        self.switch_to_the_last_window()
        # 转件选择人配置
        if not self.WorkFlowDetailConfig:
            self.WorkFlowDetailConfig = read_config("work_flow_details")
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        self.basePage.is_click(self.WorkFlowDetailConfig["作废"])
        self.basePage.input_text(self.WorkFlowDetailConfig["作废原因"], "This Is The Test Message")
        ## 如果是初始节点作废会直接作废，如果是非初始节点会启用作废流程
        btn = self.basePage.find_element(self.WorkFlowDetailConfig["启动作废流程"])
        if btn.text == "启用作废流程":
            self.basePage.is_click(self.WorkFlowDetailConfig["启动作废流程"])
            # 创建完成后会自动进入下一环节，登录所转件人账号进行校验，校验方式为切换至iframe中找寻创建件时的实例ID 的td标签
            self.click_second_pop(action=0)
            # 跳转至作废流程
            self.change_to_workflow(send_user=apply_to)
        elif btn.text == "直接作废":
            self.basePage.is_click(self.WorkFlowDetailConfig["启动作废流程"])
            self.click_second_pop(action=0)
            time.sleep(5)
            self.check_flow_create_or_false(login_user=apply_to, flow_status="作废")

    def supervise_workflow(self):
        self.switch_to_the_last_window()
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        if not self.WorkFlowDetailConfig:
            self.WorkFlowDetailConfig = read_config("work_flow_details")
        self.basePage.is_click(self.WorkFlowDetailConfig["督办"])
        self.check_flow_create_or_false(login_user=self.CreateWorkFlowUser, flow_status='督办')

    def focus_workflow(self):
        self.switch_to_the_last_window()
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        if not self.WorkFlowDetailConfig:
            self.WorkFlowDetailConfig = read_config("work_flow_details")
        self.basePage.is_click(self.WorkFlowDetailConfig["收藏"])
        self.check_flow_create_or_false(login_user=self.CreateWorkFlowUser, flow_status='关注')


    def click_second_pop(self, action=None):
        """二层弹窗，Selenium无法点击，转为使用执行JQuery语句
        作废
        退件
        """
        action = 1 if action else 0
        script = "$('span[index=%s]').click()" % action
        self.basePage.driver.execute_script(script)

    def read_workflow_loggs(self):
        self.switch_to_the_last_window()
        if not self.WorkFlowDetailConfig:
            self.WorkFlowDetailConfig = read_config("work_flow_details")
        self.basePage.is_click(self.WorkFlowDetailConfig["流程日志"])
        self.switch_to_the_last_window()
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        process_list = self.basePage.find_elements(self.WorkFlowDetailConfig["流程详情"])
        # 至少三个流程节点
        assert len(process_list) >= 3
        # 第一个节点为创建者
        # 第二个节点为开始节点
        begin_node = process_list[2]
        assert '开始节点' in begin_node.text and '办理人' in begin_node.text and '时间' in begin_node.text and '办理时限' in begin_node.text

    @staticmethod
    def get_upload_file(file_type, size, direct_path=None):
        """
        :param file_type: 文件后缀名，不同类型的文件放置在不同的文件夹
        :param size:  文件大小
        :param direct_path:  是否有指定的路径.mac不适用，适用于windows在使用自定义的文件夹时使用
        :return: mac返回单个文件的绝对路径，windows返回文件所在父文件夹的绝对路径
        """
        if G.get_sys_platform().lower() == "mac":
            # mac仅支持单个文件
            uploading_path = os.path.join(os.path.join(G.resource_path, 'upload_file_testing'), file_type)
            files = list_folder(uploading_path)
            assert files
            if not size:
                if len(files) > 2:
                    return os.path.join(uploading_path, files[random.randint(0, len(files))])
                else:
                    return os.path.join(uploading_path, files[0])
        elif G.get_sys_platform().lower() == 'windows':
            if not direct_path:
                uploading_path = os.path.join(os.path.join(G.resource_path, 'upload_file_testing'), file_type)
            else:
                uploading_path = os.path.join(
                    os.path.join(os.path.join(G.resource_path, 'upload_file_testing'), file_type), direct_path)
            files = list_folder(uploading_path)
            assert files
            return uploading_path

    def upload(self, file_type, size, node_index=0):
        if not self.WorkFlowDetailConfig:
            self.WorkFlowDetailConfig = read_config("work_flow_details")
        self.switch_to_the_last_window()
        upload_tag = self.basePage.find_elements(self.WorkFlowDetailConfig["转件材料"])
        if upload_tag:
            upload_tag = upload_tag[0]
            upload_tag.click()
            metearials = self.basePage.find_elements(self.WorkFlowDetailConfig["材料目录"])
            if not metearials:
                raise AttributeError("转件材料目录为空")
            metearials_node = self.basePage.find_elements(self.WorkFlowDetailConfig["材料袋节点"])
            log.info("右键第%s个文件节点 " % node_index)
            ActionChains(self.basePage.driver).context_click(metearials_node[node_index]).perform()
            self.basePage.is_click(self.WorkFlowDetailConfig['上传按钮'])
            this_file_path = self.get_upload_file(file_type, size)
            virtual_board = PyKeyboard()
            virtual_mouse = PyMouse()
            upload_file = []
            if G.get_sys_platform().lower() == "mac":
                virtual_board.press_keys(['Command', 'Shift', 'G'])
                virtual_board.press_keys(['Command', "A"])
                virtual_board.press_key("Delete")
                pyperclip.copy(this_file_path)
                time.sleep(2)
                virtual_board.press_keys(['Command', 'V'])

                del virtual_board
                del virtual_mouse
                virtual_board_2 = PyKeyboard()
                for i in range(10):
                    time.sleep(3)
                    virtual_board_2.press_key("return")
                    log.info("当前第%s 次按return " % i)
                time.sleep(3)
                upload_file.append(this_file_path.split("/")[-1])
            elif G.get_sys_platform().lower() == 'windows':
                virtual_board.press_key(virtual_board.function_keys[4])
                virtual_board.press_keys([virtual_board.control_key, 'a'])
                virtual_board.press_key(virtual_board.delete_key)
                # 复制路径至系统剪切板
                file_root = None
                # 重新拼接文件路径
                file_root = this_file_path.split("\\")
                file_root = '/'.join(i for i in file_root)
                pyperclip.copy(file_root)
                virtual_board.press_keys([virtual_board.control_key, 'v'])
                virtual_board.press_key(virtual_board.enter_key)
                time.sleep(3)
                virtual_mouse.click(550, 400)
                virtual_board.press_keys([virtual_board.control_key, 'a'])
                virtual_board.press_key(virtual_board.enter_key)
                upload_file = list_folder(file_root)

            self.check_work_flow_materials(filepath=upload_file, meterial_node_index=node_index)
        else:
            raise AttributeError("无转件材料选项")

    def switch_to_the_last_window(self):
        time.sleep(5)
        # 保存主窗口handle
        handles = self.basePage.driver.window_handles
        self.basePage.driver.switch_to.window(handles[-1])

    def switch_to_the_first_window(self):
        time.sleep(5)
        handles = self.basePage.driver.window_handles
        self.basePage.driver.switch_to.window(handles[0])

    def upload_files_by_folder(self):
        pass

    def check_work_flow_materials(self, filepath, meterial_node_index=0):
        """
        检查上传完成后是否有件
        :param filepath:  上传文件列表
        :param meterial_node_index: 文件 上传目录节点索引，即第几个上传文件的地方
        :return:
        """
        self.switch_to_the_last_window()
        upload_tag = self.basePage.find_elements(self.WorkFlowDetailConfig["转件材料"])
        if upload_tag:
            upload_tag = upload_tag[0]
            upload_tag.click()
            metearials = self.basePage.find_elements(self.WorkFlowDetailConfig["材料目录"])
            if not metearials:
                raise AttributeError("转件材料目录为空")
            metearials_node = self.basePage.find_elements(self.WorkFlowDetailConfig["材料袋节点"])
            metearials_node[meterial_node_index].click()

            nodes = self.basePage.find_elements(self.WorkFlowDetailConfig["材料袋节点"])
            if filepath:
                for i in filepath:
                    hit = 0
                    for j in nodes:
                        if i in j.text:
                            hit += 1
                    assert hit > 0

    def hang_on_work_flow(self, ):
        """挂起流程"""
        self.switch_to_the_last_window()
        # 转件选择人配置
        if not self.WorkFlowDetailConfig:
            self.WorkFlowDetailConfig = read_config("work_flow_details")
        if not self.instance_id:
            self.instance_id = self.get_this_instance_id()
        self.basePage.is_click(self.WorkFlowDetailConfig["流程挂起"])
        self.basePage.input_text(self.WorkFlowDetailConfig["挂起原因"], "This Is The Test Message")
        self.basePage.is_click(self.WorkFlowDetailConfig['确认挂起'])
        self.click_second_pop()
        self.check_flow_create_or_false(flow_status="挂起", login_user=self.CreateWorkFlowUser)

    def flowInstancePrint(self):
        """适配打印逻辑"""
        self.switch_to_the_last_window()
        if not self.WorkFlowDetailConfig:
            self.WorkFlowDetailConfig = read_config("work_flow_details")
        self.basePage.is_click(self.WorkFlowDetailConfig['打印'])
        self.switch_to_the_last_window()
        time.sleep(10)
        self.basePage.switch(self.WorkFlowDetailConfig['打印iframe'])
        self.basePage.is_click(self.WorkFlowDetailConfig['打印报表'])
        time.sleep(5)
        virtual_keyboard = PyKeyboard()
        virtual_keyboard.press_key('Return')
        """需要提前配置打印机，只能模拟键盘操作，按Return键"""

    def insert_options(self):
        self.basePage.input_text(self.WorkFlowDetailConfig['转件意见'], 'This is A Test Message')
