import requests
from .RequestDataSource import RequestDataSource
import logging
from bs4 import BeautifulSoup
from config.globalVars import APIGlobalVars

RequestDataSource = RequestDataSource()
logger = logging.getLogger(__name__)


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
                request_data["ticket_name"] = "ticket_password"
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
        request_data = {"username": "username",
                        "password": "password"}

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


class ZUserOrgRight(RequestBase):
    """
    各模块区分，继承至RequestBase
    一个接口一个方法，同一个接口不同的方式也分开定义
    函数定义方式为url中的/替换为_,最后_加上请求方式
    """


    def LoginApi_Gettoken_POST(self, *args, **kwargs):
        """根据用户名，密码获得登录验证token"""
        request_header = kwargs.get("request_header") if kwargs.get(
            "request_header") else RequestDataSource.RequestHeader()

        request_method = "POST"

        request_data = kwargs.get("request_data") if kwargs.get(
            "request_data") else RequestDataSource.DataSource_Login_Api_Get_Token_GET()

        request_api = "/LoginApi/getToken"

        auth = kwargs.get("auth") if kwargs.get("auth") else None

        cookie = kwargs.get("cookie") if kwargs.get("cookie") else None

        return self.begin_request(request_method=request_method, request_data=request_data,
                                  request_header=request_header, api_url=request_api,
                                  auth=auth)
