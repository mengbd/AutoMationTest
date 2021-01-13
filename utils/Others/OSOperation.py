import os
import sys
import logging
import re
from utils.Others.TimeOperation import sleep

log = logging.getLogger(__name__)


def mk_dir(path):
    # 去除首位空格
    path = path.strip()
    path = path.rstrip("\\")
    path = path.rstrip("/")

    # 判断路径是否存在
    is_exists = os.path.exists(path)

    if not is_exists:
        try:
            os.makedirs(path)
        except Exception as e:
            log.error("目录创建失败：%s" % e)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        log.debug("目录已存在：%s" % str(path))
        pass


def setPath(path, operation="add"):
    log.warning("仅windows系统可使用%s函数 " % sys._getframe().f_code.co_name)
    assert "win" in sys.platform.lower()
    if path:
        if operation == "add":
            os.environ["Path"] += path
        else:
            os.environ["Path"] -= path

        return True


def list_folder(path):
    if path:
        try:
            return os.listdir(path)
        except OSError:
            raise OSError("查找路径下文件出错")


def Ping(raw_destination):
    assert type(raw_destination) is str
    destination = raw_destination.split('.')
    if len(destination) == 4:
        for i in destination:
            assert type(eval(i)) is int
    elif len(destination) == 3:
        for i in destination:
            assert re.match(r'[\w\\:/]+', i)
    recv = os.popen('ping %s' % raw_destination)
    sleep(5)
    recv = recv.read()
    wrong = re.findall(r'Request\stimed\sout', recv)
    ttl = re.findall(r'TTL=\d+', recv)
    if not wrong and ttl:
        return True
    else:
        return False




if __name__ == "__main__":
    print(Ping('ip'))
