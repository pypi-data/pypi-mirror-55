from PythonZyjTools.get_ip_info.get_info import get_info
from PythonZyjTools.DbConnect.sqlalchemy_drivers import DBSession,engine
from PythonZyjTools.get_ip_info.message_send import message
from PythonZyjTools.get_ip_info.chuli_data import chuli
def run():
    ip_data = get_info().get_ip()
    if ip_data == None:
        chuli()
