from PythonZyjTools.DbConnect.sqlalchemy_drivers import engine,DBSession
from sqlalchemy import text
from PythonZyjTools.get_ip_info.get_ip_data_mode import get_ip_data_mode
from PythonZyjTools.Base.tools import println
from PythonZyjTools.Email.respond import email_info
from PythonZyjTools.Email.send import email_send
from PythonZyjTools import get_ip_info
from jinja2 import Environment, PackageLoader

import  os,time
class chuli:
    def __init__(self):
        self.run()
    def run(self):
        data = self.query()
        session = DBSession()

        insert_data = {
            "ip_address": "",
            "status": 0,
            "insert_time": time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),
            "executer": "none",
            "beizhu": "所有方法均失败",
            "email_send_status":"未发送"
        }

        if data[0] == 0:
            env = Environment(loader=PackageLoader("PythonZyjTools.get_ip_info", 'templates'))
            template = env.get_template("error.html")
            resource = email_info().shoujianreng(
                {"zhangyongjian": "1158477063@qq.com", "frank": "3062617007@qq.com"}).subject(
                '小艾报道：报错提醒，小哥哥快来处理').html(template.render(data=[]))
            email_send().send_email(resource)
            insert_data["email_send_status"] = "已发送"
            session.add(get_ip_data_mode(insert_data))
        else:
            insert_data["email_send_status"] = "未发送"
            session.add(get_ip_data_mode(insert_data))
        session.commit()
        session.close()


    def query(self):
        data_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "select count(*) from get_ip_data_mode where executer = 'none' and insert_time between '%s 00:00:00' and '%s 23:59:59' and email_send_status = '已发送' "%(data_now,data_now)
        source = engine.connect()
        result = source.execute(text(sql)).fetchone()
        source.close()
        return result


class ip_chuli:
    def __init__(self,data = None,session = None):
        """
        :param data: 数据
        :param session: 数据库链接session
        """
        self.data = data
        self.session = session
        self.check()
    def query_data(self):
        sql = "select t1.ip_address,t1.insert_time,t1.status,t1.executer,t1.beizhu,t1.email_send_status from (" \
              "select ip_address,insert_time,status,executer,beizhu,email_send_status " \
              "from get_ip_data_mode " \
              "where email_send_status = '已发送' and status = 1 order by insert_time desc) t1 " \
              "limit 1"
        data = engine.connect().execute(text(sql))
        result_data = []
        for i in data:
            result_data.append(i)
        if len(result_data) == 0:
            self.send_email()
            return True
        if self.data['ip_address'] != result_data[0].ip_address:
            self.send_email()
            return True
        else:
            self.zhengchang()
            println("执行时发现ip地址未发生变化")
            return False
    def check(self):
        if self.data['status'] != 1:
            self.db_save_data(self.data)
        else:
            self.query_data()
    def zhengchang(self):
        self.data['email_send_status'] = '未发送'
        self.db_save_data(self.data)
    def send_email(self):
        # package_path = os.path.dirname(get_ip_info.__file__)+'/'+
        env = Environment(loader=PackageLoader("PythonZyjTools.get_ip_info",'templates'))
        template = env.get_template("successful.html")
        resource = email_info().shoujianreng(
            {"zhangyongjian": "1158477063@qq.com", "frank": "3062617007@qq.com"}).subject(
            'IP地址发生变化:ip地址变化为' + self.data['ip_address']).html(template.render(data = self.data))
        email_send().send_email(resource)
        self.data['email_send_status'] = '已发送'
        self.db_save_data(self.data)

    def db_save_data(self,data={}):
        """
        保存数据到数据库中
        :return:
        """
        self.session.add(get_ip_data_mode(data))
        self.session.commit()
