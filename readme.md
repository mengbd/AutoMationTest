# 1 简介

基于Python，测试框架采用Pytest,API方面采用requests库，UI采用Selenium，目前适配了windows下IE、Chrome，Mac下的Chrome
暂时未适配Firefox以及Linux下的所有浏览器(linux版本太多，有需求的话可以在Issue提出或者自行二次适配)，数据库方面采用SQLAlchemy，这个用到的比较少

# 2 依赖

开发时采用Python3.9,需要以下依赖(MacOS下)，Windows上可能有些区别，可以根据报错修改

```reStructuredText
apipkg==1.5
asgiref==3.3.1
async-lru==1.0.2
attrs==20.3.0
bcrypt==3.2.0
beautifulsoup4==4.9.3
bs4==0.0.1
certifi==2020.12.5
cffi==1.14.4
chardet==4.0.0
click==7.1.2
ConfigArgParse==1.2.3
cryptography==3.3.1
cx-Oracle==6.1
defusedxml==0.6.0
diff-match-patch==20200713
EasyProcess==0.3
et-xmlfile==1.0.1
execnet==1.7.1
Flask==1.1.2
Flask-BasicAuth==0.2.0
gevent==20.9.0
geventhttpclient==1.4.5
greenlet==0.4.17
html5lib==1.1
idna==2.10
inflect==4.1.0
iniconfig==1.1.1
itsdangerous==1.1.0
jdcal==1.4.1
Jinja2==2.11.2
locust==1.4.1
lxml==4.6.1
lxmlbind==2.0
Markdown==3.3.3
MarkupPy==1.14
MarkupSafe==1.1.1
msgpack==1.0.2
mysql-connector-python==8.0.22
mysqlclient==2.0.1
openpyxl==3.0.5
packaging==20.4
paramiko==2.7.2
pika==1.1.0
pluggy==0.13.1
protobuf==3.13.0
psutil==5.8.0
py==1.9.0
pyaes==1.6.1
pycparser==2.20
pym==0.1.3
PyMySQL==0.10.1
PyNaCl==1.4.0
pyobjc-core==6.2.2
pyobjc-framework-Cocoa==6.2.2
pyobjc-framework-Quartz==6.2.2
pyparsing==2.4.7
pyperclip==1.8.1
Pyrogram==1.0.7
PySocks==1.7.1
pytest==6.1.1
pytest-assume==2.3.3
pytest-forked==1.3.0
pytest-metadata==1.10.0
pytest-parallel==0.1.0
pytest-reportlog==0.1.1
pytest-rerunfailures==9.1.1
pytest-xdist==2.2.0
python-xlib==0.29
pytz==2020.1
PyUserInput==0.1.11
PyYAML==5.3.1
pyzmq==20.0.0
requests==2.25.1
ruamel.yaml==0.16.12
ruamel.yaml.clib==0.2.2
selenium==3.141.0
six==1.15.0
soupsieve==2.0.1
sqlacodegen==2.3.0
SQLAlchemy==1.3.20
sqlparse==0.4.1
tblib==1.7.0
TgCrypto==1.2.2
toml==0.10.1
urllib3==1.26.2
webencodings==0.5.1
Werkzeug==1.0.1
zope.event==4.5.0
zope.interface==5.2.0
```



**windows下环境需要一些特别调整,Selenum上传文件采用的是虚拟键盘以及虚拟鼠标完成，依赖于Pyhook，安装步骤如下，具体可以查看工程目录/resource/windows/env/windows环境指南，环境工程下有一个已经配置好的Python38虚拟环境(windows_env.zip)**

```reStructuredText
第一步，安装pywin32，地址：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32  /////  pip install pywin32


第二步，下载pyhook_py3k，地址：https://github.com/Answeror/pyhook_py3k  ////解压即可 

第三步，下载swig.exe，地址：http://www.swig.org/download.html ///同理解压，并把解压目录添加到系统变量Path中

第四步，解压缩pyhook_py3k，并进行编译，cmd进入到setup.py的目录，执行命令：Python setup.py build_ext --swig=“这里是你的swig.exe的路径”\swigwin-3.0.12\swig.exe，可以根据实际情况修改swig.exe的路径，另外本机最好已安装VC2008

第五步，安装编译好的pyhook_py3k，命令：pip install .

第六步:  instant_client也需要添加到系统变量中
```



# 3 部分介绍

## 3.1 config 模块

工程整体配置，之前考虑过采用装饰器自动分发，但是效果不是特别明显，速度也有所下降，因此还是回退至原先的版本
即 基础配置 BaseConfig类，包含工程路径等一些基础的配置，可能全部都需要用到的配置，可以自行添加在BaseConfig类中

### 3.1.1 BaseConfig类

```python
class BaseConfig(object):
  def __init__(self, *args, **kwargs):
      self.Server_IP = "ip"
      self.Server_Port = 80 #端口
      self.root = os.path.dirname(__file__)
      self.project_root = os.path.dirname(self.root)
      self.report_path = os.path.join(self.project_root, 'report')
      self.log_path = os.path.join(self.project_root, 'log')
      self.worker = kwargs.get('worker') if kwargs.get('worker') else "AUTOMATION TEST"
      self.task_name = 'Daily'
      self.case = self.gen_case_model() if (self.task_name and self.task_name != 'Local') else None

  @staticmethod
  def get_upload_api():
  """上传结果API，如果没有可以参考我的另外一篇TestCenter博客"""
      # 可修改项
      url = 'http://ip/port/root/'
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
```

API ， UI， Database三个配置类均继承至该类，这么做的目的是测试用例代码基本上用不到别的模块的配置，避免冗余
API和Database各位看看代码就知道了，很简单，主要说一下UI

### 3.1.2 UI配置详解

代码如下

```python
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
```

可修改项均在文件中有注释，UI配置类init项中更改浏览器，初始化实例后调用set_browser方法自动配置selenium驱动，但是目前有一些弊端
**1、依赖于网络，get_driver_url方法返回驱动下载地址,默认提供的是国内镜像源，你可以自行修改，后续使用requests+bs4解析查询驱动并下载，如果本地有当前版本驱动则不会下载。如果没网可以提前下载好放到/resource/web_driver/下也可以避免，命名规则请仔细查阅代码**
**2、当你的Chrome版本是自动更新并且版本是最新，最新版本的驱动镜像站可能没有会报错，IE浏览器不会有这个问题不会，IE驱动与Selenium版本保持一致**



## 3.2 log文件夹以及report文件夹

这两个文件夹因为git设置了不同步，因此可能git clone下去的需要自己添加，log文件夹存放测试日志，report文件夹则是UI用例失败截图存放路径

## 3.3 Models文件夹

存放DataBase相关的ORM文件，默认有一个TestCaseResult，作为后续日志上传保存至数据库使用,每个键的含义翻译下英文就知道了

代码如下:

```python
class Testcaseresult(Base):
    __tablename__ = 'testcaseresult'
    id = Column(Integer, primary_key=True)
    create_worker = Column(String(30))
    create_time = Column(DATETIME(fsp=6))
    ending_worker = Column(String(30))
    ending_time = Column(DATETIME(fsp=6))
    logs = Column(LONGTEXT)
    result = Column(String(30))
    case_name = Column(String(255))
    case_number = Column(String(100))
    marker = Column(String(255))
    caselevel = Column(Integer)
    imgurl = Column(String(255))
    taskname = Column(String(255))
    request_time = Column(String(10))

    def __str__(self):
        return {
            'id': self.id,
            'create_worker': self.create_worker,
            'create_time': self.create_time,
            'ending_worker': self.ending_worker,
            'ending_time': self.ending_time,
            'logs': self.logs,
            'result': self.result,
            'case_name': self.case_name,
            'case_number': self.case_number,
            'marker': self.marker,
            'caselevel': self.caselevel,
            'imgurl': self.imgurl if self.imgurl else None,
            'taskname': self.taskname,
            'request_time': self.request_time

        }
```

上传日志的fixture在项目工程目录下的conftest.py中:

```python
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """"
    pytest后置处理fixture，无需调用，用例结束自动调用

    不能修改 该fixture负责生成日志，上传记录等。


    """
    print('------------------------------------')
    out = yield
    report = out.get_result()
    if report.when == 'call':
        logpath = os.path.join(config.log_path, "%s_%s.log" % (datetime_strftime("%Y-%m-%d_%H%M%S"), report.head_line))
        if 'win' in sys.platform:
            logpath = logpath.replace('\\', '/')
        logs = ''
        logs += "当前节点: %s " % report.nodeid + "\r"
        logs += "TestCaseName: %s   Result: %s   Duration: %sS " % (
            report.head_line, report.outcome, report.duration) + "\r"
        for i in report.sections:
            for j in i:
                if "Captured" in j:
                    logs += "-" * 20 + j + "-" * 20 + "\r"
                else:
                    logs += j + "\r"
            if report.longreprtext:
                logs += report.longreprtext + "\r"
        per_case.id = 0
        per_case.create_worker = config.worker
        per_case.result = report.outcome
        per_case.taskname = config.task_name
        per_case.ending_time = datetime_strftime()
        per_case.ending_worker = config.worker
        per_case.logs = logs
        if config.task_name != 'LOCAL':
            try:
                duration = re.findall(r'耗时\d+\.\d+', logs)
                if duration:
                    per_case.request_time = duration[0]
            except Exception as e:
                pass
            if hasattr(item, 'imgurl'):
                per_case.imgurl = item.imgurl
            saveCase(per_case)
        log_gennerator(per_case, logpath)
```

saveCase方法则是将当前实例保存，之前采用的是SQLAlchemy直连数据库保存，不过那样效率比较慢，后续改为了POST 接口的方式

保存日志至数据库，仅当config中BaseConfig中的task name不为Local时才会上传，其余任务名等我这里没加判断，你可以根据实际逻辑自行完善逻辑，如果你当前没有测试项目的接口，可以参考我的另一篇Python-web博客， TestCenter，包含很多接口(不包含前端页面)

## 3.4 resource文件夹

存放一些资源文件,包含 :

1、 instant_client(包含windows以及Mac 环境包)

Oracle数据库连接需要配置，mysql以及其他数据库可以自行存放，目的是方便其余同事配置

2、 PageElement

存放UI用例页面定位元素yml文件，具体根据各自业务存放，存放格式为 名字: 定位方式==对应定位语法
 example:

```yaml
切换iframe:  xpath==/html/body/div/div[2]/iframe
菜单: css==div > span > span
```

名字是自定义的，方便自己后续使用

3、 upload_file_testing

存放UI用例上传文件用到的样本

4、 web_driver

存放Selenium驱动，可以自己提前下载，代码自动适配存放也是在这个文件夹

5、 windows_envs

windows环境需要的一些包以及教程

## 3.5 TestCase文件夹

存放测试用例代码，分成了四个Python Package，API、 UI、 DataBase、 Others

## 3.6 utils文件夹

存放工具函数/类，也跟TestCase一样，分成了四个文件Package,>存放工具函数/类，也跟TestCase一样，分成了四个文件Package, 里边我已经封装了Selenium基类， requests基类
但根据各自业务不同，可能也需要你/您适当修改适配自己的业务才能正常启动，这里举几个小例子

### 3.6.1 RequestBase类

#### 3.6.1.1代码如下

```python
class RequestBase(object):

    def __init__(self, *args, **kwargs):

        self.ip = kwargs.get("ip")
        self.port = kwargs.get("port")
        self.body_type = kwargs.get("body_type") if kwargs.get("body_type") else "form"
        self.pattern = kwargs.get("pattern")
        self.auth = kwargs.get("auth") if kwargs.get("auth") else None
        self.ticket = kwargs.get("ticket")
        self.logger = logger
        self.cookies = kwargs.get("cookies") if kwargs.get("cookies") else None
        self.session = None

    @staticmethod
    def remake_form(data):
        """

        :param data: 请求数据 字典形式
        :return: 重组为form表单的请求body
        """
        assert type(data) is dict
        remake_data = dict()
        for i in data:
            remake_data[i] = (None, data[i])
        return remake_data

    def auth_check(self, data):
        if self.auth:
            """
            目前平台API均未加密，暂时不定义
            """
            pass
        else:
            for i in self.ticket:
                data[i] = self.ticket[i]
        return data

    def remake_url(self, api_url):
        return "http://" + self.ip + ":" + str(self.port) + "/" + self.pattern + api_url

    def begin_request(self, *args, **kwargs):
        request_data = kwargs.get("request_data")
        request_method = kwargs.get("request_method")
        request_header = kwargs.get("request_header")
        api_url = kwargs.get("api_url")
        request_url = self.remake_url(api_url) if api_url[0] != "h" else api_url
        cookies = kwargs.get("cookies") if kwargs.get("cookies") else None
        content_type = kwargs.get('content_type') if kwargs.get('content_type') else 'multipart/form-data'
        self.auth = kwargs.get("auth") if kwargs.get("auth") else None
        if request_data:
            if 'form' in content_type:
                request_data = self.remake_form(data=request_data)
                request_data = self.auth_check(request_data)
            elif 'json' in content_type:
                request_data["zjugis.api.ticket"] = "wwkj&key&zdww1402"
        self.logger.info("本地请求HEADER为 %s " % request_header)
        self.logger.info("本次请求URL为%s " % request_url)
        self.logger.info("本次请求方式为%s " % request_method)
        self.logger.info("本次请求body为%s" % request_data)
        req = None
        if self.session:
            if 'form' in content_type:
                req = self.session.request(method=request_method.upper(), url=request_url, files=request_data,
                                           headers=request_header, cookies=cookies)
            elif 'json' in content_type:
                req = self.session.request(method=request_method.upper(), url=request_url, json=request_data,
                                           headers=request_header, cookies=cookies)
        else:
            if 'form' in content_type:
                req = requests.request(method=request_method.upper(), url=request_url, files=request_data,
                                       headers=request_header, cookies=cookies)
            else:
                req = requests.request(method=request_method.upper(), url=request_url, json=request_data,
                                       headers=request_header, cookies=cookies)
        if req:
            self.logger.info("本次请求响应码为%s " % req.status_code)
            self.logger.info("本次请求Response Body为 %s" % req.text)
            self.logger.info("本次请求Response Header为 %s" % req.headers)
            self.logger.info('耗时%s' % req.elapsed.total_seconds())

            return req.status_code, req.text, req.headers

    def keep_login_alive(self):

        # 需要登录请求的API的需要先调用本方法，后续请求参数中加入cookies = self.cookies,
        # 登录状态状态保持
        request_data = {"username": "Admin",
                        "password": "zjugis1402!"}

        first_url = "http://" + self.ip + ":" + str(self.port) + "/z_user_org_right/Login/index"
        request_method = "POST"
        self.session = requests.Session()
        login_ = self.session.get(url=first_url, data=request_data, )
        assert login_.status_code == 200
        # 获取登录页
        find_redirect_url = BeautifulSoup(login_.text.split("</html>")[1], 'lxml').find_all("script")
        that = None
        for i in find_redirect_url:
            if i.contents:
                that = i.contents[0]
        that = str(that).split("\r\n")
        redirect_url = [i.strip() for i in that if "redictUrl" in i]
        assert len(redirect_url) > 0
        redirect_url = redirect_url[0].split("'")[-2]
        validate_url = "http://" + self.ip + ":" + str(self.port) + "/z_user_org_right/Login/validate"
        request_data["redictUrl"] = redirect_url
        validate_user = self.session.post(validate_url, data=request_data)
        assert validate_user.status_code == 200
        self.session_set_cookie(request_data["username"], request_data["password"])

    def session_set_cookie(self, name, password):
        self.session.cookies["%s_pwd" % name] = password
```

**session_set_cookie keep_login_alive auth_check remake_form这四个方法中的一些逻辑需要你根据自身业务调整，这几个方法主要覆盖保存session，登录状态保持，以及是否需要重新拼接url， auth方式等，一定要修改**

#### 3.6.1.2 设计目的

封装一个基类，各位的业务应该都不是一整个模块，分很多场景，抽取基本请求方法以及认证，后续每个模块一个类，继承至RequestBase，添加该模块API方法即可
举个例子:

```python
class ZUserOrgRight(RequestBase):
    """
    各模块区分，继承至RequestBase
    一个接口一个方法，同一个接口不同的方式也分开定义
    函数定义方式为url中的/替换为_,最后_加上请求方式
    """

    def Login_Api_Get_Token_GET(self, *args, **kwargs):
        request_header = kwargs.get("request_header") if kwargs.get(
            "request_header") else RequestDataSource.RequestHeader()

        request_method = "GET"

        request_data = kwargs.get("request_data") if kwargs.get(
            "request_data") else RequestDataSource.DataSource_Login_Api_Get_Token_GET()

        request_api = "/LoginApi/getToken"

        auth = kwargs.get("auth") if kwargs.get("auth") else None

        cookie = kwargs.get("cookie") if kwargs.get("cookie") else None

        return self.begin_request(request_method=request_method, request_data=request_data,
                                  request_header=request_header, api_url=request_api,
                                  auth=auth)
```

这样后续测试代码将各模块代码区分，不会重复交叉，设计用例fixture时即可每个模块设置一个fixture，独立区分
这里举一个fixture例子:

```python
@pytest.fixture(scope="function")
def example_USER_fixture(request):
    USER_FIXTURE = ZUserOrgRight(pattern="/z_user_org_right", ip=config.Server_IP,
                                 port=config.Server_Port, ticket=config.Server_Checking_ticket)
    yield USER_FIXTURE
```

测试用例调用该fixture后，可以直接使用fixture返回的实例请求接口，也许你会问fixture怎么用，这里再举一个用例例子，关于fixture以及其余pytest装饰器的用法，请查阅pytest官方文档或者github给我提issue

```python
@pytest.mark.TestCase("[1]测试获取登录API验证是否正常")
def test_Login_Api_Get_Token_GET(preInit, example_USER_fixture):
    sss = example_USER_fixture.Login_Api_Get_Token_GET()
    preInit.info("沙发沙发上")
```

### 3.6.2 UI Selenium基类

#### 3.6.2.1 代码
基于这个基类我封装了一个WorkFLowActions_Release.py，这个只是给大家作为一个示范使用，需要结合自己业务流程重新封装，我这个请不要使用，没有任何作用

```python
class WebPage(object):
    """selenium基类"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = G.TIME_OUT
        self.wait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """打开网址并验证"""
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            log.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(G.LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)

    def find_elements(self, locator):
        """查找多个相同的元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def switch(self,locator):
        sleep(0.5)
        ele = self.find_element(locator)
        log.info("切换至定位元素为%s%s的ifraeme" % locator)
        self.driver.switch_to.frame(ele)

    def input_text(self, locator, txt):
        """输入(输入前先清空)"""
        sleep(0.5)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)
        log.info("输入文本：{}".format(txt))

    def is_click(self, locator):
        """点击"""
        self.find_element(locator).click()
        sleep()
        log.info("点击元素：{}".format(locator))

    def element_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        log.info("获取文本：{}".format(_text))
        return _text

    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)

    def url(self):
        return self.driver.current_url
```



#### 3.6.2.2 UI-driver fixture

同API fixture类似，UI也提供了DEMO fixture,不过UI需要考虑到失败截图等，因此UI用例文件夹的fixture有三个

**关于fixture的用法，以及定义方式等，请查阅pytest文档**

```python
import pytest

from selenium import webdriver
from config.globalVars import UIGlobalVars
from utils.HTTPRequest.HttpRequest import uploadFileToServer
from utils.Others.TimeOperation import datetime_strftime
import logging

log = logging.getLogger(__name__)
config = UIGlobalVars()
driver = None


@pytest.fixture(scope='session', autouse=False)
def drivers(request):
    """
    driver fixture ,UI相关用例使用，根据G变量中browser检测驱动，如果没有则自动下载，
    :param request:
    :return:
    """
    global driver
    if not driver:
        config.set_browser()
        driver_path = config.DRIVER_PATH
        if config.browser.upper() == "CHROME":
            driver = webdriver.Chrome(executable_path=driver_path)
        else:
            driver = webdriver.Ie(executable_path=driver_path)
        driver.maximize_window()

    def fn():
        driver.quit()

    request.addfinalizer(fn)
    return driver


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """UI相关用例执行失败自动截图 """
    # 获取钩子方法的调用结果
    out = yield
    # 3. 从钩子方法的调用结果中获取测试报告
    report = out.get_result()
    if report.when == 'call' and report.outcome == "failed":
        path1 = str(report.nodeid)
        path2 = path1.split("::")[-1]
        png_path = config.report_path + "\\%s_%s.png" % (datetime_strftime(fmt='%Y-%m-%d_%H%M%S'), path2)
        _capture_screenshot(png_path)
        try:
            url = uploadFileToServer(png_path)
            setattr(item, 'imgurl', url)
        except Exception as e:
            setattr(item, 'imgurl', png_path)
            log.info('上传截图失败,保存至本地,请检查连接')



def _capture_screenshot(path):
    '''
    截图保存为png
    :return:
    '''
    return driver.get_screenshot_as_file(path)

```

# 4 结尾

以上就是关于项目的简介，也许无法覆盖得很全面，如果你有疑问，可以在下方留言，或者github提issue，我收到后会尽快回复(本站回复仅使用noreply@oslozone.cn的邮箱账号，其余回复请直接作废)

# 5 项目地址

欢迎Star 欢迎ISSUE

GitHub: 

[GitHub-AutoMationTest](https://github.com/oslo254804746/AutoMationTest)

Gitee(China)

[Gitee-AutoMationTest](https://gitee.com/oslo254804746/AutoMationTest)

# 6 特别致谢
感谢JetBrains对于本项目的大力支持 
[JetBrain](https://jb.gg/OpenSource)
