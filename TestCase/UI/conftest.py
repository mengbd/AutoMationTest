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
    print('------------------------------------')
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
