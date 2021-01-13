import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.testing import entities


class DataBaseOperation(object):

    def __init__(self, configs):
        os.environ["NLS_LANG"] = "GERMAN_GERMANY.UTF8"  # 解决中文乱码
        config = None
        data_base_account = None
        for k, v in configs.items():
            config = v
            data_base_account = k
        data_base_ip = config.get("ip")
        data_base_listener_port = config.get("ListenerPort")
        data_base_instance_name = config.get('InstanceName')
        data_base_password = config.get("password")
        data_base_mode = config.get('mode') if config.get('mode') else None
        self.db_engine = None
        self.meta = None

        if data_base_ip and data_base_password and data_base_listener_port and data_base_instance_name and data_base_account and data_base_password:
            if not data_base_mode:
                self.db_engine = sqlalchemy.create_engine('oracle+cx_oracle://%s:%s@%s:%s/%s' % (
                    data_base_account, data_base_password, data_base_ip, data_base_listener_port, data_base_instance_name
                ), echo=True,)
            else:
                self.db_engine = sqlalchemy.create_engine('oracle+cx_oracle://%s:%s@%s:%s/%s?mode=%s' % (
                    data_base_account, data_base_password, data_base_ip, data_base_listener_port, data_base_instance_name, data_base_mode
                ), echo=True,)

            session_maker = sessionmaker(bind=self.db_engine)
            self.session = session_maker()

    """
    原先使用的方法全部删除，改为使用session自带
    """


class DataBaseOperationMysql(object):
    """
    Mysql
    db = DataBaseOperationMysql({'user': '', 'port': '', 'host': '', 'database': '','password':''})

    """

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')
        password = kwargs.get('password')
        host = kwargs.get('host')
        port = kwargs.get('port')
        database = kwargs.get('database')
        if not user or not password or not host or not port or not database:
            return
        Base = declarative_base()
        engine = sqlalchemy.create_engine(
            "mysql+pymysql://%s:%s@%s:%s/%s" % (user, password, host, port, database),
            encoding="utf-8",
            echo=True
        )
        Base.metadata.create_all(engine)
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()
