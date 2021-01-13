# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, NVARCHAR, Table, Text, VARCHAR, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DEPARTMENTCopy(Base):
    __tablename__ = 'DEPARTMENT_copy'
    __table_args__ = {'comment': '???'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    name = Column(NVARCHAR(64), comment='????')
    simple_name = Column(NVARCHAR(64), comment='????')
    dept_code = Column(VARCHAR(64), comment='????')
    address = Column(NVARCHAR(64), comment='??')
    telephone = Column(VARCHAR(32), comment='??')
    fax = Column(VARCHAR(32), comment='??')
    pid = Column(VARCHAR(36), index=True, comment='????ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    bz = Column(NVARCHAR(255), comment='??')


class Branche(Base):
    __tablename__ = 'branche'
    __table_args__ = {'comment': '?????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    name = Column(VARCHAR(255), comment='??????')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    bz = Column(VARCHAR(255), comment='??')


class Department(Base):
    __tablename__ = 'department'
    __table_args__ = {'comment': '???'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    name = Column(NVARCHAR(64), comment='????')
    simple_name = Column(NVARCHAR(64), comment='????')
    dept_code = Column(VARCHAR(64), comment='????')
    address = Column(NVARCHAR(64), comment='??')
    telephone = Column(VARCHAR(32), comment='??')
    fax = Column(VARCHAR(32), comment='??')
    pid = Column(VARCHAR(36), index=True, comment='????ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    bz = Column(NVARCHAR(255), comment='??')
    isinformal = Column(NUMBER(3, 0, False), server_default=text("0 "), comment='????????')


class DeptRelBranche(Base):
    __tablename__ = 'dept_rel_branche'
    __table_args__ = {'comment': '??????????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    department_id = Column(VARCHAR(36), comment='??ID')
    branche_id = Column(VARCHAR(36), comment='????ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class DeptRelLeader(Base):
    __tablename__ = 'dept_rel_leader'
    __table_args__ = {'comment': '???????????????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    user_id = Column(VARCHAR(36), comment='??id')
    department_id = Column(VARCHAR(36), comment='??ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class DeptRelUser(Base):
    __tablename__ = 'dept_rel_user'
    __table_args__ = {'comment': '???????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    user_id = Column(VARCHAR(36), comment='??ID')
    department_id = Column(VARCHAR(36), comment='??ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class District(Base):
    __tablename__ = 'district'
    __table_args__ = {'comment': '?????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    city_code = Column(VARCHAR(4), index=True, comment='????')
    city_name = Column(NVARCHAR(64), comment='????')
    county_code = Column(VARCHAR(2), comment='????')
    county_name = Column(NVARCHAR(64), comment='????')
    town_code = Column(VARCHAR(3), comment='????')
    town_name = Column(NVARCHAR(64), comment='????')
    village_code = Column(VARCHAR(3), comment='???')
    village_name = Column(NVARCHAR(64), comment='???')
    group_code = Column(VARCHAR(2), comment='???')
    group_name = Column(NVARCHAR(64), comment='???')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    bz = Column(NVARCHAR(255), comment='??')
    full_code = Column(VARCHAR(14), index=True, comment='????')


t_gh_rel_user = Table(
    'gh_rel_user', metadata,
    Column('z_user_org_right_id', VARCHAR(255)),
    Column('z_user_org_right_name', VARCHAR(255)),
    Column('??????', VARCHAR(255)),
    Column('userid', VARCHAR(255)),
    Column('username', VARCHAR(255)),
    Column('password', VARCHAR(255)),
    Column('passwordsalt', VARCHAR(255)),
    Column('displayname', VARCHAR(255)),
    Column('shortname', VARCHAR(255)),
    Column('usertype', VARCHAR(255)),
    Column('createtime', VARCHAR(255)),
    Column('description', VARCHAR(255)),
    Column('isconfirmed', VARCHAR(255)),
    Column('confirmationtoken', VARCHAR(255)),
    Column('islockedout', VARCHAR(255)),
    Column('email', VARCHAR(255)),
    Column('nickname', VARCHAR(255)),
    Column('weight', VARCHAR(255)),
    Column('iconid', VARCHAR(255)),
    Column('zwpass', VARCHAR(255)),
    Column('sindex', VARCHAR(255)),
    Column('wechatid', VARCHAR(255))
)


class GroupBelongtoUser(Base):
    __tablename__ = 'group_belongto_user'
    __table_args__ = {'comment': '???????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    belongto_user_id = Column(VARCHAR(36), comment='????ID')
    group_id = Column(VARCHAR(36), comment='??ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    i_creator = Column(NUMBER(asdecimal=False), comment='??????1?? 0???')
    group_authority = Column(NUMBER(asdecimal=False), comment='?????1???? 0????')


class KeyValue(Base):
    __tablename__ = 'key_value'
    __table_args__ = {'comment': 'key-value???'}

    id = Column(VARCHAR(50), primary_key=True, comment='??ID')
    key = Column(NVARCHAR(64), comment='?')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    value = Column(Text, comment='?')


class Leader(Base):
    __tablename__ = 'leader'

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    user_id = Column(VARCHAR(36), comment='??ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class LoginPage(Base):
    __tablename__ = 'login_page'

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    name = Column(NVARCHAR(64), comment='????')
    redirecturl_app = Column(NVARCHAR(256), comment='?????????')
    externalurl_app = Column(NVARCHAR(256), comment='?????????')
    redirecturl_web = Column(NVARCHAR(256), comment='WEB???????')
    externalurl_web = Column(NVARCHAR(256), comment='WEB???????')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    i_enable = Column(NUMBER(asdecimal=False), comment='????  1?????? 2??')
    page_mark = Column(NVARCHAR(64), comment='????')
    i_ca = Column(NUMBER(asdecimal=False), comment='??CA??')


class LoginPageHtml(Base):
    __tablename__ = 'login_page_html'
    __table_args__ = {'comment': '???HTML'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    web_html = Column(Text, comment='WEB?HTML')
    app_html = Column(Text, comment='APP?HTML')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????\x13')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    login_page_id = Column(VARCHAR(36), index=True, comment='???Id')


class ObjectPromisstion(Base):
    __tablename__ = 'object_promisstion'
    __table_args__ = {'comment': '????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    object_type = Column(NVARCHAR(64), comment='???? ????/??/??')
    object_value = Column(VARCHAR(36), comment='???  ?????/???/???? ?ID')
    promisstion_type = Column(NVARCHAR(64), comment='????????.???.????  ??ZJUGIS.WORKFLOW.TEMPLATE')
    promisstion_value = Column(VARCHAR(36), comment='????ID?  ??????ID(36????)')
    p_promisstion_vaule = Column(VARCHAR(36), comment='?????ID???????ID(36????)')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class OrgChangeLog(Base):
    __tablename__ = 'org_change_log'
    __table_args__ = {'comment': '??????????????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    classify = Column(NUMBER(asdecimal=False), comment='???? ??12?????;1?????;4?????;9??????')
    content = Column(NVARCHAR(256), comment='????')
    op_date = Column(DateTime, comment='????')
    user_name = Column(VARCHAR(64), comment='???')
    user_id = Column(VARCHAR(36), comment='????ID')
    real_name = Column(NVARCHAR(64), comment='??????')
    ip = Column(VARCHAR(16), comment='?????IP??')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    isok_num = Column(VARCHAR(10), comment='?????? ?6/6?')


class Position(Base):
    __tablename__ = 'position'
    __table_args__ = {'comment': '???'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    name = Column(NVARCHAR(64), comment='??')
    p_department_id = Column(VARCHAR(36), comment='????ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    code = Column(NVARCHAR(64), comment='??')
    type = Column(NUMBER(asdecimal=False), comment='????  0 ???? 10?????')


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'comment': '???'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    name = Column(NVARCHAR(64), comment='???')
    classify = Column(NVARCHAR(64), comment='????')
    i_default = Column(NUMBER(asdecimal=False), comment='??????   0??  1??')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz = Column(NVARCHAR(255), comment='??')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class RoleRelUser(Base):
    __tablename__ = 'role_rel_user'
    __table_args__ = {'comment': '???????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    user_id = Column(VARCHAR(36), comment='??ID')
    role_id = Column(VARCHAR(36), comment='??ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class SsoService(Base):
    __tablename__ = 'sso_service'
    __table_args__ = {'comment': '??????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    system_name = Column(NVARCHAR(64), comment='????')
    login_url = Column(NVARCHAR(256), comment='??????')
    logout_url = Column(NVARCHAR(256), comment='??????')
    token = Column(VARCHAR(256), comment='????')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    i_enable = Column(NUMBER(asdecimal=False), comment='????')


class SyncLog(Base):
    __tablename__ = 'sync_log'
    __table_args__ = {'comment': '?????????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    change_id = Column(VARCHAR(36), comment='????ID')
    i_ok = Column(NUMBER(asdecimal=False), comment='?????? 1??  0??')
    errorinfo = Column(NVARCHAR(500), comment='????')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class SyncService(Base):
    __tablename__ = 'sync_service'
    __table_args__ = {'comment': '??????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    website_name = Column(NVARCHAR(64), comment='????')
    service_url = Column(VARCHAR(256), comment='????')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    i_enable = Column(NUMBER(asdecimal=False), comment='???? 1??????  0??')


class ThirdParty(Base):
    __tablename__ = 'third_party'

    id = Column(VARCHAR(36), primary_key=True)
    third_party_name = Column(VARCHAR(255))
    index_code = Column(NUMBER(asdecimal=False))
    create_worker = Column(VARCHAR(36))
    create_time = Column(DateTime)
    latest_modify_worker = Column(VARCHAR(255))
    latest_modify_time = Column(DateTime)
    isvalid = Column(NUMBER(asdecimal=False))
    bz1 = Column(NVARCHAR(255))
    bz2 = Column(NVARCHAR(255))
    bz3 = Column(NVARCHAR(255))
    bz4 = Column(NVARCHAR(255))
    bz = Column(NVARCHAR(255))


class ThirdPartyLinkWorker(Base):
    __tablename__ = 'third_party_link_worker'
    __table_args__ = {'comment': '?????????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??id')
    third_party_id = Column(NVARCHAR(512), comment='?????id')
    worker_id = Column(NVARCHAR(36), comment='??id')
    index_code = Column(Integer, comment='????')
    create_worker = Column(NVARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(NVARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(Integer, comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    third_party_name = Column(NVARCHAR(512), comment='???????')


class UserBelongtoGroup(Base):
    __tablename__ = 'user_belongto_group'
    __table_args__ = {'comment': '???????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    user_id = Column(VARCHAR(36), comment='??ID')
    belongto_group_id = Column(VARCHAR(36), comment='????ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


t_user_import = Table(
    'user_import', metadata,
    Column('??', VARCHAR(255)),
    Column('????', VARCHAR(255)),
    Column('???', VARCHAR(255))
)


class UserLink(Base):
    __tablename__ = 'user_link'
    __table_args__ = {'comment': '???????'}

    user_id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    third_user_id = Column(NVARCHAR(64), index=True, comment='?????ID')
    third_type = Column(NVARCHAR(36), index=True, comment='????? ??-dd ??-wx ??')


class UserRelDistrict(Base):
    __tablename__ = 'user_rel_district'
    __table_args__ = {'comment': '????????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    user_id = Column(VARCHAR(36), nullable=False, comment='??ID')
    district_id = Column(VARCHAR(36), nullable=False, comment='????ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class UserRelPosition(Base):
    __tablename__ = 'user_rel_position'
    __table_args__ = {'comment': '???????'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    user_id = Column(VARCHAR(36), comment='??ID')
    position_id = Column(VARCHAR(36), comment='??ID')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': '???'}

    id = Column(VARCHAR(36), primary_key=True, comment='??ID')
    login_name = Column(NVARCHAR(64), comment='???')
    real_name = Column(NVARCHAR(64), comment='????')
    pinyin_name = Column(VARCHAR(64), comment='????')
    password = Column(VARCHAR(64), comment='??')
    sex = Column(NUMBER(asdecimal=False), comment='??  1??  2??')
    email = Column(VARCHAR(64), comment='????')
    telephone = Column(VARCHAR(32), comment='????')
    mobilephone = Column(VARCHAR(32), comment='??')
    id_card = Column(VARCHAR(32), comment='???')
    worker_state = Column(NUMBER(asdecimal=False), comment='????   10???;   20??? ;  99???;     ???? ')
    worker_type = Column(NUMBER(asdecimal=False), comment='????   10????? 20?????? 30????')
    extend1 = Column(NVARCHAR(255), comment='????1')
    extend2 = Column(NVARCHAR(255), comment='????2')
    extend3 = Column(NVARCHAR(255), comment='????3')
    extend4 = Column(NVARCHAR(255), comment='????4')
    e_signature = Column(NVARCHAR(256), comment='????  ??URL')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
    bz = Column(NVARCHAR(255), comment='??')
    is_leader = Column(NUMBER(asdecimal=False), comment='????  ???????? 0????? 1?')
    ca_key = Column(VARCHAR(64))
    worker_level = Column(NUMBER(asdecimal=False), comment='????')


t_users0814 = Table(
    'users0814', metadata,
    Column('id', VARCHAR(36), nullable=False),
    Column('login_name', NVARCHAR(64)),
    Column('real_name', NVARCHAR(64)),
    Column('pinyin_name', VARCHAR(64)),
    Column('password', VARCHAR(64)),
    Column('sex', NUMBER(asdecimal=False)),
    Column('email', VARCHAR(64)),
    Column('telephone', VARCHAR(32)),
    Column('mobilephone', VARCHAR(32)),
    Column('id_card', VARCHAR(32)),
    Column('worker_state', NUMBER(asdecimal=False)),
    Column('worker_type', NUMBER(asdecimal=False)),
    Column('extend1', NVARCHAR(255)),
    Column('extend2', NVARCHAR(255)),
    Column('extend3', NVARCHAR(255)),
    Column('extend4', NVARCHAR(255)),
    Column('e_signature', NVARCHAR(256)),
    Column('index_code', NUMBER(asdecimal=False)),
    Column('create_worker', VARCHAR(36)),
    Column('create_time', DateTime),
    Column('latest_modify_worker', VARCHAR(36)),
    Column('latest_modify_time', DateTime),
    Column('isvalid', NUMBER(asdecimal=False)),
    Column('bz1', NVARCHAR(255)),
    Column('bz2', NVARCHAR(255)),
    Column('bz3', NVARCHAR(255)),
    Column('bz4', NVARCHAR(255)),
    Column('bz', NVARCHAR(255)),
    Column('is_leader', NUMBER(asdecimal=False)),
    Column('ca_key', VARCHAR(64)),
    Column('worker_level', NUMBER(asdecimal=False))
)


class UsersGroup(Base):
    __tablename__ = 'users_group'
    __table_args__ = {'comment': '??'}

    id = Column(VARCHAR(36), primary_key=True, comment='??')
    name = Column(NVARCHAR(64), comment='????')
    index_code = Column(NUMBER(asdecimal=False), comment='????')
    create_worker = Column(VARCHAR(36), comment='???')
    create_time = Column(DateTime, comment='????')
    latest_modify_worker = Column(VARCHAR(36), comment='?????')
    latest_modify_time = Column(DateTime, comment='??????')
    isvalid = Column(NUMBER(asdecimal=False), comment='????')
    bz1 = Column(NVARCHAR(255), comment='??1')
    bz2 = Column(NVARCHAR(255), comment='??2')
    bz3 = Column(NVARCHAR(255), comment='??3')
    bz4 = Column(NVARCHAR(255), comment='??4')
