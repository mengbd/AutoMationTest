import yaml
import os
import pytest

from config.globalVars import G


class RunScripts():

    def __init__(self):
        curPath = os.path.dirname(os.path.realpath(__file__))
        yamlPath = os.path.join(curPath, "config.yaml")
        f = open(yamlPath, 'r', encoding='utf-8')
        datas = f.read()
        self.run_config = yaml.load(datas)
        self.rerun = self.run_config["失败重跑次数"]
        self.rerun_delay = self.run_config["失败重跑延时"]
        self.test_collection = None

    def parse(self):

        if self.run_config["运行模式"] == "ByFilename":
            assert self.run_config["文件名"] != '[]'
            self.parse_file()
        elif self.run_config["运行模式"] == "ByCasename":
            assert self.run_config["用例名"] != '[]'
        else:
            raise AttributeError("Unsupported RunTime Config")

    def parse_file(self):
        file_path = self.run_config["文件名"]
        file_path_true = []
        try:
            file_name_generator =  os.walk(os.path.join(G.project_root, "TestCase"))
            for root, dirs, files in file_name_generator:
                for file in files:
                    if file in file_path:
                        file_path_true.append(os.path.join(root,file))
                        print("已找到%s ,当前进度%s" % (file, file_path.index(file) / len(file_path)))
            print("已找到%s 个 文件, 一共%s个， 找寻进度 %s" % (len(file_path_true), len(file_path), len(file_path_true)/len(file_path_true)))
            self.test_collection = file_path_true
        except Exception as e:
            raise OSError("找寻测试文件地址错误")

    def parse_case(self):
        try:
            case_li = self.run_config["用例名"]
            case_name_file = []
            file_name_generator = os.walk(os.path.join(G.project_root, "TestCase"))
            for root, dirs, files in file_name_generator:
                for file in files:
                    if file.endswith(".py"):
                        with open(os.path.join(root, file), 'r') as f :
                            datas = f.read()
                            for i in case_li:
                                if i in datas:
                                    case_name_file.append(os.path.join(root, file) + "::" + i)
            print("找到%s个用例，一共%s个，找寻完成率%s" % (len(case_name_file), len(case_li) , len(case_name_file)/len(case_li)))
            self.test_collection = case_name_file
        except Exception as e:
            raise OSError("Find Case File Goes Wrong!")

    def start(self):
        self.parse()
        args = ['--reruns', str(self.rerun),'--reruns-delay', str(self.rerun_delay), '-v', ]
        args += self.test_collection
        pytest.main(args)


if __name__ == "__main__":
    task = RunScripts()
    task.start()