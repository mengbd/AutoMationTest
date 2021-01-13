from sqlalchemy import Column, VARCHAR, Integer, create_engine, DateTime, String
from sqlalchemy.dialects.mysql import LONGTEXT, DATETIME
from sqlalchemy.ext.declarative import declarative_base
import requests
import json

Base = declarative_base()
metadata = Base.metadata


class Testcaseresult(Base):
    __tablename__ = 'testcaseresult'

    id = Column(Integer, primary_key=True)
    create_worker = Column(String(30))
    create_time = Column(DATETIME(fsp=6))
    ending_worker = Column(String(30))
    ending_time = Column(DATETIME(fsp=6))
    logs = Column(LONGTEXT)
    result = Column(String(30))
    case_name = Column(String(255))
    case_number = Column(String(100))
    marker = Column(String(255))
    caselevel = Column(Integer)
    imgurl = Column(String(255))
    taskname = Column(String(255))
    request_time = Column(String(10))

    def __str__(self):
        return {
            'id': self.id,
            'create_worker': self.create_worker,
            'create_time': self.create_time,
            'ending_worker': self.ending_worker,
            'ending_time': self.ending_time,
            'logs': self.logs,
            'result': self.result,
            'case_name': self.case_name,
            'case_number': self.case_number,
            'marker': self.marker,
            'caselevel': self.caselevel,
            'imgurl': self.imgurl if self.imgurl else None,
            'taskname': self.taskname,
            'request_time': self.request_time

        }


engine = create_engine("mysql+pymysql://username:password@ip:3306/databasename",
                       max_overflow=5)  # 创建引擎


def init_db():  # 初始化表
    Base.metadata.create_all(bind=engine)


def getModel():
    cmd = r"""sqlacodegen oracle+cx_oracle://TESTCASE:password\!@ip:1521/test --outfile filename.py"""
    mysql = '''sqlacodegen mysql+pymysql://TestCenterUser:password!@ip:3306/testcenter --outfile 
    filename.py '''


def saveCase(instance):
    ##目前采用通过SQlalchemy方式来记录，后续更换为通过POST方式增加记录

    # Session_class = sessionmaker(bind=engine)
    # Session = Session_class()
    # try:
    #     Session.add(instance)
    # except Exception as e:
    #     Session.rollback()
    # Session.commit()
    # Session.close_all()
    datas = instance.__str__()
    req = requests.post('http://ip:83/api/caselog/', json=datas)

    assert req.status_code == 201



