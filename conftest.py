import pytest
import os
import sys
import re
sys.path.append(os.path.dirname(__file__))
import logging
from config.globalVars import BaseConfig
from utils.Others.TimeOperation import datetime_strftime
from Models.TestCase import Testcaseresult, saveCase

"""
总工程的conftest为pytest工程共享配置，每个测试函数均可调用，
各个测试模块文件夹中定义的fixture仅仅该文件夹下的代码可以调用
fixture可以实现各种初始化，后置处理
"""
config = BaseConfig()
per_case = Testcaseresult()
log = logging.getLogger(__name__)


def log_gennerator(instance, path):
    if instance.logs and path:
        path = path.encode('utf-8').decode('unicode_escape')
        with open(path, 'w+') as f:
            f.write(instance.logs)


def pytest_runtest_setup(item):
    for mark in item.iter_markers(name="TestCase"):
        print("TestCase args={} kwargs={}".format(mark.args, mark.kwargs))
        sys.stdout.flush()


@pytest.fixture(scope="function", autouse=True, )
def preInit(request, *args, **kwargs):
    """初始化fixture 返回log对象
    fixture可以调用其他fixture
    """
    log.info("Start Setting UP " + "\r")
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    filepath = request.node.nodeid
    per_case.create_time = datetime_strftime()
    log.info("TestCase: %s Start, Using Fixtures: %s " % (filepath, str(request.fixturenames)))
    per_case.caselevel = request.node.own_markers[0].args[0].split("]")[0][1]
    per_case.case_name = request.node.own_markers[0].args[0].split("]")[1]
    per_case.case_number = request.node.name
    per_case.marker = request.node.own_markers[0].name
    log.info("UsingMarker: %s CaseLevel: Level %s CaseName:%s" % (
        per_case.marker, per_case.caselevel, per_case.case_name) + "\r")
    return log


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """"
    pytest后置处理fixture，无需调用，用例结束自动调用

    不能修改 该fixture负责生成日志，上传记录等。


    """
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
