import datetime
import json
import zipfile
import re
from email.mime.multipart import MIMEMultipart

import yaml
import os
import pytest
from config.globalVars import BaseConfig
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText

from email.header import Header

G = BaseConfig()


def GetRunConfig() -> dict:
    """解析config.yaml"""
    curPath = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(curPath, "config.yaml")
    f = open(yamlPath, 'r', encoding='utf-8')
    datas = f.read()
    return yaml.load(datas)


class RunScripts:

    def __init__(self):
        self.run_config = GetRunConfig()
        self.rerun = self.run_config["ReRunTimes"]
        self.rerun_delay = self.run_config["ReRunDelay"]
        self.test_collection = None

    def parse(self):

        if self.run_config["RunMode"] == "ByFilename":
            assert self.run_config["FileName"]
            self.parse_file()
        elif self.run_config["RunMode"] == "ByCasename":
            assert self.run_config["CaseName"]
            self.parse_case()
        else:
            raise AttributeError("Unsupported RunTime Config")

    def parse_file(self):
        file_path = self.run_config["FileName"]
        file_path_true = []
        try:
            file_name_generator = os.walk(os.path.join(G.project_root, "TestCase"))
            for root, dirs, files in file_name_generator:
                for file in files:
                    if file in file_path:
                        file_path_true.append(os.path.join(root, file))
                        print("已找到%s ,当前进度%s" % (file, file_path.index(file) / len(file_path)))
            print("已找到%s 个 文件, 一共%s个， 找寻进度 %s" % (
                len(file_path_true), len(file_path), len(file_path_true) / len(file_path_true)))
            self.test_collection = file_path_true
        except Exception as e:
            raise OSError("找寻测试文件地址错误")

    def parse_case(self):
        try:
            case_li = self.run_config["CaseName"]
            case_name_file = []
            file_name_generator = os.walk(os.path.join(G.project_root, "TestCase"))
            for root, dirs, files in file_name_generator:
                for file in files:
                    if file.endswith(".py"):
                        with open(os.path.join(root, file), 'r') as f:
                            datas = f.read()
                            for i in case_li:
                                if 'def ' + i in datas:
                                    case_name_file.append(os.path.join(root, file) + "::" + i)
            print("找到%s个用例，一共%s个，找寻完成率%s" % (len(case_name_file), len(case_li), len(case_name_file) / len(case_li)))
            self.test_collection = case_name_file
        except Exception as e:
            raise OSError("Find Case File Goes Wrong!")

    def start(self):
        self.parse()
        args = ['--reruns', str(self.rerun), '--reruns-delay', str(self.rerun_delay), '-v', ]
        args += self.test_collection
        with open(os.path.join(G.root, 'config.json'), 'rb') as f:
            f.write(json.dumps(self.run_config['TaskConfig']))
        if self.run_config['ExecTime']:
            try:
                startTime = datetime.datetime.strptime(self.run_config['ExecTime'], '%Y-%m-%d %H:%M:%S', )
                nowTime = datetime.datetime.now()
            except Exception as e:
                return
            if startTime > nowTime:
                self.set_sheduler(args)
            else:
                return
        else:
            self.startTest(args)

    def set_sheduler(self, args):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.startTest, 'date', run_date=self.run_config['ExecTime'], args=(args,))

    @staticmethod
    def startTest(args):
        logs = os.listdir(G.log_path)
        for i in logs:
            os.remove(os.path.join(G.log_path, i))
        pytest.main(args)

    def send_task_email(self):
        mail_host = self.run_config['SendUserConfig']['host']
        mail_user = self.run_config['SendUserConfig']['user']
        mail_port = self.run_config['SendUserConfig']['port']
        mail_password = self.run_config['SendUserConfig']['password']
        receivers = self.run_config['NotifiEmailAddress']
        mail_message = """以下是您的测试结果，请查收"""
        message = MIMEMultipart()
        message.attach(MIMEText(mail_message, 'html', 'utf-8'))
        message['From'] = Header("TestNotification", 'utf-8')
        message['To'] = Header("TestNotification", 'utf-8')
        subject = "测试结果邮件"
        message['Subject'] = Header(subject, 'utf-8')
        sender = self.run_config['SendUserConfig']['user']
        log_zip = self.gen_log_zip()
        with open(log_zip, 'rb') as f:
            datas = f.read()
        content = MIMEText(datas, 'base64', 'utf-8')
        content["Content-Type"] = 'application/octet-stream'
        content["Content-Disposition"] = 'attachment; filename=%s' % re.split(r'[\\/]', log_zip)[-1]
        message.attach(content)

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, mail_port)
            smtpObj.login(mail_user, mail_password)
            smtpObj.sendmail(sender, receivers, message.as_string())
        except smtplib.SMTPException:
            raise smtplib.SMTPException

    @staticmethod
    def gen_log_zip(log_dir=G.log_path):
        result_dir = log_dir + '.zip'  # 压缩后文件夹的名字

        z = zipfile.ZipFile(log_dir, 'w', zipfile.ZIP_DEFLATED)
        for dir_path, dir_names, file_names in os.walk(log_dir):
            f_path = dir_path.replace(log_dir, '')
            f_path = f_path and f_path + os.sep or ''
            for filename in file_names:
                z.write(os.path.join(dir_path, filename), f_path + filename)
        z.close()
        return result_dir

    def __del__(self):
        if self.run_config['NotifiEmailAddress'] and ('' not in self.run_config['SendUserConfig'].values()):
            self.send_task_email()
        del self


DEMO_CONFIG = {'RunMode': 'ByFilename',
               'FileName': ['test_z_workflow_api', 'test_z_web_container_api'],
               'CaseName': [], 'ReRunTimes': 1,
               'ReRunDelay': 5, 'TaskName': 'Daily',
               'ProjectRoot': '/TEST_AUTOMATION/',
               'ExecTime': datetime.datetime(2021, 2, 4, 14, 6),
               'NotifiEmailAddress': ['test@test.com'],
               'SendUserConfig': {'username': '', 'password': '', 'POP3': ''}}

if __name__ == "__main__":
    task = RunScripts()
    task.start()
