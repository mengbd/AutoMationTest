import os
import subprocess
import re
import sys
import json
import logging
import zipfile
import requests
import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from Models.TestCase import Testcaseresult
from utils.Others.OSOperation import Ping


log = logging.getLogger(__name__)


class BaseConfig(object):

    def __init__(self, *args, **kwargs):
        self.Server_IP = "ip"
        self.Server_Port = 82
        self.root = os.path.dirname(__file__)
        self.project_root = os.path.dirname(self.root)
        self.report_path = os.path.join(self.project_root, 'report')
        self.log_path = os.path.join(self.project_root, 'log')
        self.worker = kwargs.get('worker') if kwargs.get('worker') else "AUTOMATION TEST"
        self.task_name = 'Daily'
        self.case = self.gen_case_model() if (self.task_name and self.task_name != 'Local') else None

    @staticmethod
    def get_upload_api():
        # 可修改项 执行记录保存接口 替换为自己的接口
        url = 'http://ip:port/apis/caseresult/'
        return url

    @staticmethod
    def gen_case_model():
        case = Testcaseresult()
        return case

    def upload_case_detail(self, case):
        if not case:
            return
        request = requests.post(self.get_upload_api(), json.dumps(case))
        return True if request.status_code == 201 else False


class APIGlobalVars(BaseConfig):

    def __init__(self):
        super().__init__()
        self.UploadFileAPI = "/z_file_management/FileInfoApi/uploadFileByOtherSystem"
        self.Auth_Method = ''  # 可修改项，认证方式
        self.Server_Checking_ticket = {"ticket_name": (None, "ticket_password")}
        if self.Auth_Method:
            self.Server_Checking_Username = ""
            self.Server_Checking_password = ""


class DataBaseGlobalVars(BaseConfig):

    def __init__(self):
        super().__init__()
        self.data_base_config = {
            'Z_AUTO_DEPLOY':
                {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                 'InstanceName': 'develop'},
            'Z_USER_ORG_RIGHT':
                {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                 'InstanceName': 'develop'},
            'Z_BUSSINESS_COMMOM':
                {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                 'InstanceName': 'develop'},
            'Z_FILE_MANAGEMENT':
                {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                 'InstanceName': 'develop'},
            'Z_MIDDLEWARE_MQ':
                {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                 'InstanceName': 'develop'},
            'Z_SPRING_DEMO':
                {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                 'InstanceName': 'develop'},
            'Z_WORKFLOW':
                {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                 'InstanceName': 'develop'},
            'Z_WEB_CONTAINER':
                {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                 'InstanceName': 'develop'},
            'sys': {'ip': 'ip', 'ListenerPort': 1521, 'password': 'password',
                    'InstanceName': 'develop', 'mode': 'SYSDBA'}, }


class UIGlobalVars(BaseConfig):
    def __init__(self):
        super().__init__()
        self.retry_times = 3
        self.TIME_OUT = 30
        self.resource_path = os.path.join(self.project_root, "resource")
        self.web_driver_path = os.path.join(self.resource_path, "webdriver")
        self.ELEMENT_PATH = os.path.join(os.path.dirname(self.web_driver_path), "PageElement")
        self.browser = "IE"  # 可修改项,浏览器类型,当前支持IE以及Chrome
        self.DRIVER_PATH = None
        self.browser_version = None
        # 定位元素语法
        self.LOCATE_MODE = {
            'css': By.CSS_SELECTOR,
            'xpath': By.XPATH,
            'name': By.NAME,
            'id': By.ID,
            'class': By.CLASS_NAME,
        }
        self.req_version = None

    @staticmethod
    def get_driver_url(browser):
        url = {
            "IE": "https://npm.taobao.org/mirrors/selenium/",
            "CHROME": "https://npm.taobao.org/mirrors/chromedriver/"
        }
        return url.get(browser.upper())

    @staticmethod
    def get_chrome_browser_reg(platform):
        browser_root = {"Chrome": {"MAC": r"/Applications/Google\ Chrome.app/Contents/MacOS/",
                                   "WINDOWS": r"SOFTWARE\Google\Chrome\BLBeacon"
                                   }}
        return browser_root.get("Chrome").get(platform.upper())

    @staticmethod
    def get_sys_platform():
        platform = sys.platform
        if 'darwin' in platform:
            return 'mac'
        elif 'win' in platform:
            return 'windows'
        elif 'linux' in platform:
            return "linux"

    def set_browser(self):
        platform = self.get_sys_platform()
        if self.browser.upper() == "CHROME":
            if "mac" in platform:
                result = subprocess.Popen(
                    [r'{}/Google\ Chrome --version'.format(self.get_chrome_browser_reg(platform))],
                    stdout=subprocess.PIPE, shell=True)
                self.browser_version = [x.decode("utf-8") for x in result.stdout][0].strip().split(" ")[-1]
                log.warning("您的电脑为 %s 平台, 浏览器为 %s 版本号 %s " % (platform, self.browser, self.browser_version))
            elif "win" in platform:
                import winreg
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.get_chrome_browser_reg(platform))
                    self.browser_version = winreg.QueryValueEx(key, "version")[0]
                except Exception:
                    raise Exception("查询注册表chrome版本失败!")
                log.warning("您的电脑为 %s 平台, 浏览器为 %s 版本号 %s " % (platform, self.browser, self.browser_version))
        elif "win" in platform and self.browser.upper() == "IE":
            log.warning("您的电脑为 %s 平台，浏览器为 %s" % (platform, self.browser,))
            self.browser_version = selenium.__version__
        file_vr = self.search_ver()
        if not file_vr:
            raise Exception("未获取到版本号! 请检查!")
        status, file = self.check_driver(file_vr)
        if not status:
            log.warning("未查询到本地驱动")
            self.gen_driver(file_vr)
        else:
            log.warning("系统已存在%sdriver, 无需下载!" % self.browser)
            self.DRIVER_PATH = os.path.join(self.web_driver_path, file)

    def search_ver(self):
        if self.browser_version:
            file_vr = None
            if self.browser.upper() == "CHROME":
                if Ping(self.get_driver_url(self.browser)):
                    log.info('当前网络能够连接')
                    number = self.browser_version.split(".")[0]
                    url = self.get_driver_url(self.browser) + self.browser_version + '/'
                    r = requests.get(url)
                    bs = BeautifulSoup(r.text, 'lxml')
                    record = "{}/{}/notes.txt".format(self.get_driver_url(self.browser), self.browser_version)
                    info = requests.get(record)
                    text = info.text
                    vr = re.findall(r"-+ChromeDriver\s+(\d+\.+\d+\.\d+\.\d+)", text)
                    br = re.findall(r'Supports\sChrome\s+version\s+(\d+)', text)
                    if number in br and self.browser_version in vr:
                        log.info("找到浏览器对应驱动版本号: {}".format(self.browser_version))
                        file_vr = self.browser_version
                    else:
                        log.info('当前版本为最新，未找到驱动，尝试使用当前大版本最新的驱动')
                        latest_url = self.get_driver_url(self.browser)
                        req = requests.get(latest_url)
                        soup = BeautifulSoup(req.text, 'lxml')
                        a_tag = soup.find_all(name='a')
                        like_vr = self.browser_version.split(".")
                        like_vr.pop(-1)
                        like_vr = like_vr[0] + '.' + like_vr[1]+'.' + like_vr[2]
                        like_list = list()
                        for i in a_tag:
                            if i.text.startswith(like_vr):
                                like_list.append(i.text[:-1])
                        file_vr = max(like_list)
                else:
                    log.warning('当前网络不通，默认检测本地是否还有驱动!')
                    file_vr = self.browser_version
            elif self.browser.upper() == "IE":
                assert self.get_sys_platform() == 'windows'
                if self.browser_version.endswith('0'):
                    self.req_version = self.browser_version[:-2]
                if Ping(self.get_driver_url(self.browser)):
                    log.info('当前网络可连通')
                    url = self.get_driver_url(self.browser) + self.req_version + "/"
                    r = requests.get(url)
                    bs = BeautifulSoup(r.text, 'lxml')
                    url_list = bs.find_all(['a'])
                    vr = "Win32_%s" % self.browser_version
                    v_l = []
                    for i in url_list:
                        v_l.append(i.attrs['href'])
                    if vr in str(v_l):
                        log.info("找到浏览器对应驱动版本号: {}".format(file_vr))
                        file_vr = vr
                else:
                    log.warning('当前无网络连接')
                    file_vr = "Win32_%s" % self.browser_version
            return file_vr

    def check_driver(self, file_vr):
        status, filename = False, None
        if os.path.exists(self.web_driver_path):
            pass
        else:
            os.mkdir(self.web_driver_path)
        for root, dirs, files in os.walk(self.web_driver_path):
            for file in files:
                if file_vr not in file:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception:
                        continue
                else:
                    status, filename = True, file

        return status, filename

    def gen_driver(self, file_vr):
        if Ping(self.get_driver_url(self.browser)):
            if file_vr:
                driver = None
                file = None
                r = None
                if self.browser.upper() == "CHROME":
                    if self.get_sys_platform() == "mac":
                        file = "chromedriver_mac64.zip".format(file_vr)
                        driver = "chromedriver"
                    elif "windows" == self.get_sys_platform():
                        file = "chromedriver_win32.zip".format(file_vr)
                        driver = "chromedriver.exe"
                    else:
                        file = "chromedriver_linux64.zip".format(file_vr)
                        driver = "chromedriver"
                    r = requests.get("{}{}/{}".format(self.get_driver_url(self.browser), file_vr, file))
                elif self.browser == "IE":
                    file = "IEDriverServer_{}.zip".format(file_vr)
                    driver = "IEdriverServer.exe"
                    r = requests.get(
                        "{}{}/IEDriverServer_{}.zip".format(self.get_driver_url(self.browser), self.req_version, file_vr))
                file_path = os.path.join(self.web_driver_path, file)
                log.info("开始下载!")
                with open(file_path, "wb") as f:
                    f.write(r.content)
                self.unzip_driver(file)
                self.change_driver_name(file_vr, driver)
        else:
            raise KeyboardInterrupt("无网络连接，且本地无驱动")

    def get_browser_version(self):

        kernel = sys.platform
        if "darwin" in kernel:
            chrome_app = r"/Applications/Google\ Chrome.app/Contents/MacOS/"
        elif "win" in kernel:
            platform = "windows"
            chrome_reg = r"SOFTWARE\Google\Chrome\BLBeacon"

    def unzip_driver(self, filename):
        if self.get_sys_platform() == "mac":
            os.system('cd {};unzip {}'.format(self.web_driver_path, filename))
            os.path.join(self.web_driver_path, filename)
        elif self.get_sys_platform() == "windows":
            self.unzip_win(os.path.join(self.web_driver_path, filename))
            os.remove(os.path.join(self.web_driver_path, filename))

    def change_driver_name(self, version, filename):
        if self.get_sys_platform() == "mac":
            new_file = "{}_{}".format(filename, version)
        elif self.get_sys_platform() == "windows":
            L = filename.split(".")
            new_file = "{}_{}.{}".format("".join(L[:-1]), version, L[-1])
        else:
            new_file = ""
        os.rename(os.path.join(self.web_driver_path, filename),
                  os.path.join(self.web_driver_path, new_file))
        self.DRIVER_PATH = os.path.join(self.web_driver_path, new_file)

    def unzip_win(self, filename):
        with zipfile.ZipFile(filename) as f:
            for names in f.namelist():
                f.extract(names, self.web_driver_path)
