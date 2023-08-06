# -*- coding: utf-8 -*-
import socket,paramiko
import os,random,time
from PythonZyjTools.LinuxConnect.security import security
class Create_Connect(security):
    timeout = 3
    resource = None
    data = {}
    #未实例对象
    __instance = None
    def __init__(self,ip='',user='',password='',port=22):
        super().__init__(self,ip,user,password,port)
        self.info={"ip":ip,"user":user,"password":password,"port":port}
        self.init()
    def loading_check_data(self,ip,user,password,port):
        """
        处理传入参数，格式化参数
        return 返回self
        """
        self.data['ip'] = str(ip)
        self.data['user'] = str(user)
        self.data['password'] = str(password)
        self.data['port'] = int(port)
        if self.data['ip'] == '' or self.data['user'] =='' or self.data['password'] == '':
            return {"status":False,"info":'请确认ip，用户，密码参数传输完毕?'}
        if Create_Connect.ping(self.data['ip'],self.data['port']) == False:
            return {"status":False,"info":'机器'+str(ip)+'不在线，或端口'+ str(port) +'未开放'}           
        return {"status":True}
    def init(self):
        result = self.loading_check_data(self.info["ip"],self.info["user"],self.info["password"],self.info["port"])
        if result["status"] != True :
            raise Exception(result["info"])
        self.connect()
    # 静态方法用于验证网络连通
    @staticmethod
    def ping(ip,port):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(Create_Connect.timeout)
        try:
            sk.connect((ip, port))
            result = True
        except Exception:
            result = False
        finally:
            sk.close()
        return result
    def connect(self):
        if self.resource == None:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.data['ip'], username=self.data['user'], password=self.data['password'],port=self.data['port'])
            # 返回基础通道对象用于上传下载
            self.transport = client.get_transport()
            #返回资源
            self.resource = client
        return self
    def close(self):
        if self.resource != None:
            print("关闭资源中")
            self.resource.close()
            self.resource = None
    """
    运行一条指令
    """
    def run_command(self,start_command = ''):
        try:
            stdin, stdout, stderr = self.resource.exec_command(start_command,get_pty=True)
            return stdout.readlines()
        except:
            return None
    """
    上传一个脚本，设置为777权限
    """
    def upload_jiaoben(self,file_path='',remote_path ='',permission=777,cacher=True):

        if file_path.split() == '' or remote_path.split() == '' or len(file_path) == 0:
            return False
        # 格式化目录
        remote_path = remote_path.replace('\\', '/')
        command = 'mkdir -p ' + remote_path
        self.resource.exec_command(command)
        # 打开SFTP客户端
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        # 设置权限
        sftp.chmod(remote_path, permission)
        if cacher != True:
            #打开目标的路径列出文件列表
            values = sftp.listdir(remote_path)
            remote_file_name = os.path.basename(file_path)
            if remote_file_name.split() in values:
                while remote_file_name not in values:
                    remote_file_name = time.strftime('%Y-%m-%d-%H-%M-%S|', time.localtime(time.time()))+remote_file_name

        remote_path_file = os.path.join(remote_path, os.path.basename(file_path)).replace('\\', '/')
        sftp.put(file_path, remote_path_file)


        代谢该
        #########################################


        try:
            if file_path == '':
                print('脚本地址不能为空..')
                return None
            command = 'mkdir -p ' + remote_path
            self.resource.exec_command(command)
            sftp =paramiko.SFTPClient.from_transport(self.transport)
            sftp.chdir(os.path.dirname(remote_path))
            sftp.chmod(remote_path, 777)
            values = sftp.listdir(os.path.dirname(remote_path))
            remote_path_file = os.path.join(remote_path,os.path.basename(file_path)).replace('\\', '/')
            sftp.put(file_path,remote_path_file)
            sftp.chmod(remote_path_file,777)
            print("上传到了远程路径：",remote_path_file)
            return remote_path_file
        except Exception as e:
            print(e)
            return None
    def have_file(self,remote_path):
        """
        检测该文件到底存不存在
        :return:
        """
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        try:
            dir_name = os.path.dirname(remote_path)
            base_name = os.path.basename(remote_path)
            values = sftp.listdir(dir_name)
            if base_name in values:
                return True
            else:
                return False
        except:
            print('远程打印出现异常',remote_path)
            return False

    """
    运行一个远程机器上的脚本，并得到返回结果
    """
    def run_jiaoben(self,path):
        try:
            cmd = path
            stdin, stdout, stderr = self.resource.exec_command(cmd)
            values = stdout.readlines()
            return values
        except:
            return None
    """
    上传一个脚本，并执行脚本返回结果
    """
    def exec_jiaoben(self,file_path='',remote_path =''):
        try:
            path = self.upload_jiaoben(file_path=file_path,remote_path =remote_path)
            if path == None:
                return path
            return self.run_jiaoben(path)
        except:
            return None
    def close(self):
        # 关闭资源
        pass


