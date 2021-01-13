import requests
import logging
from utils.Others.TimeOperation import datetime_strftime
import json

log = logging.getLogger(__file__)


def uploadFileToServer(filepath):
    uploadFileUrl = 'http://ip:83/api/uploadFile/'
    file = {'image': open(filepath, 'rb')}
    req = requests.post(url=uploadFileUrl, files= file)
    assert req.status_code == 200
    url = json.loads(req.text)
    return url.get('url')



if __name__ == "__main__":
    uploadFileToServer(filepath='../../report/2020-12-29 14:22:14_test_loginPlatform.png')
