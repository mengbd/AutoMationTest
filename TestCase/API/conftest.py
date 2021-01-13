import pytest
from utils.HTTPRequest.RequestBase import ZUserOrgRight
from config.globalVars import APIGlobalVars

config = APIGlobalVars()


@pytest.fixture(scope="function")
def example_USER_fixture(request):
    USER_FIXTURE = ZUserOrgRight(pattern="/z_user_org_right", ip=config.Server_IP,
                                 port=config.Server_Port, ticket=config.Server_Checking_ticket)
    return USER_FIXTURE


