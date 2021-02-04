import logging

import pytest
from utils.UI.WebPage.WorkFlowActions_Release import WorkFlowActions

log = logging.getLogger(__file__)


@pytest.mark.TestCase("[1]新建详情，转件成功，且对应首页能查看到记录")
def test_demo(drivers):
    driver = drivers
    try:
        create_workflow = WorkFlowActions(driver)
        create_workflow.login()
    except Exception as e:
        raise e


@pytest.mark.usefixtures("WorkFlowPage")
class TestWorkFlowProcessing:

    @pytest.mark.TestCase("[1]正常转件(基本操作)")
    def test_normal_send_workflow(self):
        assert self.page
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '基本操作'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(menu_name=menu_name, tag_name=tag_name)
        log.info('转件给Test2账户')
        self.page.change_to_workflow(send_user='test2')
        log.info('转件给Test3账户')
        self.page.change_to_workflow(send_user='test3')
        log.info('使用Test3账户归档， 并查看已完成页签下是否有对应的实例')
        self.page.change_to_workflow(flow_status='已完成', send_user='test3')

    @pytest.mark.TestCase("[1]转件意见填写(意见填写)")
    def test_send_workflow_with_opinions(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '意见填写'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(menu_name=menu_name, tag_name=tag_name)
        log.info('转件给Test2账户')
        self.page.change_to_workflow(send_user='test2', options=True)
        log.info('转件给Test3账户')
        self.page.change_to_workflow(send_user='test3')
        log.info('使用Test3账户归档， 并查看已完成页签下是否有对应的实例')
        self.page.change_to_workflow(flow_status='已完成', send_user='test3')

    @pytest.mark.TestCase("[1]附件材料上传(附件材料上传)")
    def test_send_workflow_with_upload_file(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '附件材料上传'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(menu_name=menu_name, tag_name=tag_name)
        self.page.upload(file_type='xlsx', node_index=0, size=0)
        self.page.change_to_workflow(send_user='test2')
        self.page.change_to_workflow(send_user='test3')
        self.page.change_to_workflow(send_user='test3', flow_status='已完成')

    @pytest.mark.TestCase("[1]正常转件同级转件(基本操作)")
    def test_send_workflow_with_the_same_level(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '基本操作'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(menu_name=menu_name, tag_name=tag_name)
        self.page.change_to_workflow_with_same_level(send_user='test2')
        self.page.change_to_workflow(send_user='test3')
        self.page.change_to_workflow(send_user='test3', flow_status='已完成')

    @pytest.mark.TestCase("[1]子流程转件(子流程测试)")
    def test_change_to_workflow_with_children_instance(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '子流程测试'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.change_to_workflow(send_user='test2', is_child=True)
        self.page.change_to_workflow(send_user='test3')
        self.page.change_to_workflow(send_user='test4')
        self.page.change_to_workflow(send_user='test5', is_child=True)
        log.info('校验test5账户上有父流程归档件')
        self.page.change_to_workflow(send_user='test5', flow_status='已完成')
        log.info('校验test4账户上有子流程归档件')
        self.page.instance_id, self.page.parent_flow_id = self.page.parent_flow_id, self.page.instance_id
        self.page.check_flow_create_or_false(login_user='test4', flow_status='已完成')

    @pytest.mark.TestCase("[1]正常转件挂起(基本操作)")
    def test_hang_up_flow(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '基本操作'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.hang_on_work_flow()

    @pytest.mark.TestCase("[1]正常转件作废(基本操作)")
    def test_drop_work_flow(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '基本操作'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.drop_workflow(apply_to='test1')

    @pytest.mark.TestCase("[1]正常转件督办(基本操作)")
    def test_supervise_workflow(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '基本操作'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.supervise_workflow()

    @pytest.mark.TestCase("[1]正常转件流程日志(基本操作)")
    def test_workflow_logs(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '基本操作'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.change_to_workflow(send_user='test2')
        self.page.change_to_workflow(send_user='test3')
        self.page.change_to_workflow(send_user='test3', flow_status='已完成')
        self.page.read_workflow_loggs()

    @pytest.mark.TestCase('[1]正常转件收藏(基本操作)')
    def test_focus_workflow(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '基本操作'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.focus_workflow()

    @pytest.mark.TestCase("[1]正常转件正常退件(基本操作)")
    def test_return_workflow(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '基本操作'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.change_to_workflow(send_user='test2')
        self.page.return_message(login_user='test1')
        self.page.change_to_workflow(send_user='test2')
        self.page.change_to_workflow(send_user='test3')
        self.page.change_to_workflow(send_user='test3', flow_status='已完成')

    @pytest.mark.TestCase("[1]活动选项-自动转件-活动自动转件(自动转件)")
    def test_auto_archive_workflow(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '自动转件'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.change_to_workflow(send_user='test2')
        self.page.change_to_workflow(send_user='test3', flow_status='已完成', auto=True)

    @pytest.mark.TestCase("[1]活动选项-自动转件-活动自动转件(自动转件)-多人")
    def test_auto_archive_workflow_multiple(self):
        log.info('使用Test1账号登陆')
        self.page.login(login_user='test1')
        menu_name = '自动化测试目录'
        tag_name = '自动转件'
        log.info('点击 - {}-{}'.format(menu_name, tag_name))
        self.page.create_work_flow(tag_name=tag_name, menu_name=menu_name)
        self.page.change_to_workflow(send_user='test2')
        send_user = ['test3', 'test4', 'test5']
        self.page.change_to_workflow_multiple(send_user=send_user)
        for i in send_user:
            self.page.check_flow_create_or_false(login_user=i)
            self.page.change_to_workflow(flow_status='已完成', send_user=i)
