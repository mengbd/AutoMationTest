import datetime
import re

def convert_time(time_string, fmt="%Y%m%d-%H%M%S"):
    # 仅ORM使用，
    return datetime.datetime.strptime(time_string, fmt)


def replace_space(string):
    re.sub(r'[\n\r]', '', string)
    return string


if __name__ == "__main__":
    print(replace_space(str({"connectByGatewayDto": """{"flowTemplateVersionId": "","prevProcessId": "","nextProcessIds": 
        [""]}"""})))