from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy,time

Base = declarative_base()

class get_ip_data_mode(Base):
    __tablename__ = 'get_ip_data_mode'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True)
    ip_address = sqlalchemy.Column(sqlalchemy.String(20))
    insert_time = sqlalchemy.Column(sqlalchemy.DATETIME,nullable=False,default='0')
    status = sqlalchemy.Column(sqlalchemy.Integer,default=0,nullable=False)
    executer = sqlalchemy.Column(sqlalchemy.String(255),default='',nullable=False)
    beizhu = sqlalchemy.Column(sqlalchemy.String(255),default='')
    email_send_status = sqlalchemy.Column(sqlalchemy.String(20),default='未发送')
    def __init__(self,data={}):
        for i in data:
            if hasattr(self,i):
                if str(type(getattr(self,i))) != "<class 'method'>":
                    setattr(self,i,data[i])


