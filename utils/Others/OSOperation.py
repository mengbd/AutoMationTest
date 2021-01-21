import os
import subprocess
import sys
import logging
import re
import tempfile

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
        raw_destination = destination[0].split("//")[-1] + '.' + destination[1] + '.' + destination[2].split("/")[0]
    wrong = True
    ttl = None
    if 'win' not in sys.platform or 'darwin' in sys.platform:
        out_temp = tempfile.SpooledTemporaryFile()
        fileno = out_temp.fileno()
        ex = subprocess.Popen('ping %s -c4' % raw_destination, stdout=fileno, stderr=fileno, shell=True)
        ex.wait(5)
        out_temp.seek(0)
        lines = out_temp.readlines()

        for i in lines:
            print(i)
        lines = str(lines)
        # out, err = ex.communicate()
        wrong = re.findall(r'Request\stimed\sout', lines)
        ttl = re.findall(r'ttl=\d+', lines)
    else:
        out_temp = tempfile.SpooledTemporaryFile()
        fileno = out_temp.fileno()
        ex = subprocess.Popen('ping %s' % raw_destination, stdout=fileno, stderr=fileno, shell=True)
        ex.wait(5)
        out_temp.seek(0)
        lines = out_temp.readlines()

        for i in lines:
            print(i)
            lines[lines.index(i)] = i.decode('gbk')
        lines = str(lines)
        wrong = re.findall(r'找不到主机', lines)
        ttl = re.findall(r'TTL=\d+', lines)

    if not wrong and ttl:
        return True
    else:
        return False




if __name__ == "__main__":
    print(Ping('ip'))
