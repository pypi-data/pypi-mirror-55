# -*- coding: utf-8 -*-
import re

class get_info:
    def __init__(self, resource):
        self.source = resource
        if resource.resource == None:
            raise RuntimeError('所引入的linux连接资源为None，不通过,请重新检查linux资源是否可用')

    """
    获取linux版本
    """

    def version(self):
        version = self.source.run_command('cat /etc/redhat-release')
        if version != None:
            if version[0].strip(' ') == '':
                return None
            return version[0].strip('\n')
        else:
            return None

    """
    获取linux sn
    """

    def sn(self):
        sn_linux = self.source.run_command("dmidecode -t 1|grep UUID")
        pattern = re.compile(r'(.*)?\n$', re.S)
        for i in range(len(sn_linux)):
            items = re.findall(pattern, sn_linux[i])[0]
            sn_linux[i] = items
        str_sn = ','.join(sn_linux)
        return str_sn.strip(' ')

    """
    获得端口号
    """

    def port(self):
        port_linux = self.source.run_command("netstat -plnt|awk '{print$4}'")
        port_linux.remove('(only\n')
        port_linux.remove('Local\n')
        pattern = re.compile(r'([0-9]*)?\n$', re.S)
        for i in range(len(port_linux)):
            items = re.findall(pattern, port_linux[i])[0]
            port_linux[i] = items
        str_port = ','.join(port_linux)
        return str_port

    """
    获得目标的mac地址
    """

    def mac_linux(self):
        try:
            mac_info = self.source.run_command('ifconfig')
            mac_string = " ".join(mac_info)
            ip = self.source.data['ip'].replace(".", r"\.")
            zifu = r'.*?' + ip + r'.*?ether(.*?)txqueuelen'
            pattern = re.compile(zifu, re.S)
            items = re.findall(pattern, mac_string)
            if len(items) == 0:
                zifu = r'HWaddr(.*?)inet.*?addr:' + ip
                pattern = re.compile(zifu, re.S)
                items = re.findall(pattern, mac_string)
                if len(items) == 0:
                    print("正则表达式:" + zifu)
                    result = ""
                else:

                    result = items[0]
                    print(items)
            else:
                result = items[0]
        except:
            result = ""
        finally:
            return result

    """
    获取目标计算机的cpu核数
    """

    def cpu_core(self):
        try:
            cpu_info = self.source.run_command('cat /proc/cpuinfo| grep "cpu cores"| uniq')
            cpu_info_string = " ".join(cpu_info).strip().replace('\n', '').replace('\r', '')
        except:
            cpu_info_string = ""
        finally:
            return cpu_info_string

    """
    获取目标计算机的cpu型号
    """

    def cpu_model(self):
        try:
            cpu_info = self.source.run_command('cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c')
            cpu_info_string = " ".join(cpu_info).strip().replace('\n', '').replace('\r', '')
        except:
            cpu_info_string = ""
        finally:
            return cpu_info_string

    """
    获取目标计算机的cpu型号
    """

    def memory(self):
        try:
            memory_info = self.source.run_command("free -h |grep Mem|awk '{print$2}'")
            memory_info_string = " ".join(memory_info).strip().replace('\n', '').replace('\r', '')
        except:
            memory_info_string = ""
        finally:
            return memory_info_string

    def check_exec_online(self, data):
        try:
            jieguo = self.source.run_command("ps -ef |grep %s |grep -v grep|awk '{print $2}'" % (data['service_path']))
            if len(jieguo) >= 1 and jieguo[0].split() != "":
                return True
            else:
                return False
        except:
            return None

    def __del__(self):
        print("关闭资源中")
        if self.source != None and self.source.resource != None:
            self.source.close()
# 使用案例
# xiaojian = linux_drives.linux(ip='192.168.1.89',user='root',password='xiaojian5791041')
#
# print(get_info(xiaojian).version())
