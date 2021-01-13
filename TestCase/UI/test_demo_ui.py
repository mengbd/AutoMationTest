import pytest
import time
from utils.UI.WebPage.WorkFlowActions_Beta import SendWorkFlow, MultiStepWorkFlow
from utils.UI.WebPage.WorkFlowActions_Release import WorkFlowActions


@pytest.mark.TestCase("[1]新建详情，转件成功，且对应首页能查看到记录")
def test_demo(preInit, drivers):
    driver = drivers
    log = preInit
    try:
        create_workflow = SendWorkFlow(driver)
        log.info("开始登录平台")
        create_workflow.login()
        log.info("点击创建流程按钮")
        create_workflow.create_work_flow()
        log.info("开始转件")
        time.sleep(10)
        log.info("测试转件是否完成")
        create_workflow.change_to_workflow()
    except Exception as e:
        raise e

