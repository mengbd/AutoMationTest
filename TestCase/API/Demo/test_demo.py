import pytest


@pytest.mark.TestCase("[1]根据用户名，密码获得登录验证token,获取接口响应时间")
def test_LoginApi_Gettoken_POST(preInit, User_org_right):
    logger = preInit
    Api = User_org_right
    try:
        request_data = {
            "name": "yucw",
            "pwd": "123456"
        }
        logger.info("开始请求接口")
        request_result = Api.LoginApi_Gettoken_POST(request_data=request_data)
        logger.info("校验请求响应码200")
        assert 200 == request_result[0]
        logger.info("校验响应body不为空且无报错")
        assert '' != request_result[1] and "error" not in str(request_result[1])
        response_example = {"id": "df0a28e3-0c82-4e40-9d95-54cd3e83c327",
                            "token": "F42808612FDC077FFD0194750198BB3537A48592769BC96778B1335D383708465001C3ED046E423B369E88699B9D757072439D3210EEA4C15667A8BD1D10F472A29341DC0DB2323E"}
        for i in response_example:
            assert i in str(request_result[1])
    except Exception as e:
        raise e



