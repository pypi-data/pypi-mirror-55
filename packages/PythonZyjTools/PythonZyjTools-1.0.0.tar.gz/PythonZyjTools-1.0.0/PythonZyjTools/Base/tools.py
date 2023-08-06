'''
@Description: 一些小工具
@Author: 张永健
@Date: 2019-08-26 13:07:38
@LastEditTime: 2019-08-26 13:10:02
@LastEditors: Please set LastEditors
'''
import time
def println(string = ''):
    """
    快速打印一些信息
    :param string:
    :return:
    """
    print(time.strftime('%Y.%m.%d %H:%M:%S |', time.localtime(time.time())) ,string,'|信息类型：',type(string))