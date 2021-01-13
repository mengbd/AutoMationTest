# -*- coding:utf-8 -*-
import time
import os
from locust import HttpUser, task
import json


def remake_form(data):
    Server_Checking_ticket = {"ticket_name": (None, "ticket_password")}
    assert type(data) is dict
    request_form = dict()
    for i in data:
        request_form[i] = (None, data[i])
    for k, v in Server_Checking_ticket.items():
        request_form[k] = v
    return request_form


class QuickStartUser(HttpUser):

    def func(self, response):
        print(response.text)
        if response.status_code != 200 or response.text == '':
            print('返回异常')
            print("请求返回状态码:", response.status_code)

        else:
            print('返回正常')

    @task
    def test_sfsfs(self):
        r = self.client.get(
            url='/ecgap_kcdj/Flow/djsh?flowInstanceId=0176906e9c4cf40107ab769047c80207&activityInstanceId=017690869b68f40107ab769047c8028b&_fm=0171e9b34eee0001890471e7f55b0008&participant=017690869b68f40107ab769047c8028c&userId=fadd0d57-43fb-4374-88f8-b99df8320fba&status=1&child=0&sourcewindowid=handlerCaseCenter',
            cookies={"i_ca": "0", "zjugis.file.size": "314572800",
                     "ticket": "6333DB013C6DD56C533B5786C0B12D1337A48592769BC967DF9351F8872A4CB701414C3252D18BCEF8052532F59D6070BB6F76C3633823CC8D90B3C9EBD260ADF4DABCE8B4A4AF95"})
        self.func(r)


if __name__ == "__main__":
    os.system('locust -f test_locust.py --host=http://2.20.42.42:8088')
