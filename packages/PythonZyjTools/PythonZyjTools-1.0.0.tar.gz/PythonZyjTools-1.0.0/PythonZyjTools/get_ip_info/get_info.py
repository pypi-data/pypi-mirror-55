import requests,re,time,traceback
from selenium import webdriver
from PythonZyjTools.Base.tools import println
from selenium.webdriver.chrome.options import Options
from PythonZyjTools.DbConnect.sqlalchemy_drivers import DBSession
from PythonZyjTools.get_ip_info.get_ip_data_mode import get_ip_data_mode
from PythonZyjTools.get_ip_info.chuli_data import ip_chuli

class get_info:
    def __init__(self):
        pass
    def get_ip(self):
        result = get_ip_source_one().get_ip()
        if result != None:
            return result
        result = get_ip_source_two().get_ip()
        if result != None:
            return result

class get_ip_base:
    """
    所有实现类的基类
    """
    pass

class get_ip_source_one(get_ip_base):
    """
    获取ip的第一种方法
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.session = DBSession()
    def get_ip(self):
        """
        获取ip地址
        :return:
        """
        try:
            # 设置无界面操作
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            # 调入参数实现无界面操作
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.get("http://192.168.1.1/")
            pattern = re.compile('.*<li.*?(请输入管理员密码)</li>.*?', re.S)
            items = re.findall(pattern, browser.page_source)
            if len(items) != 0 and type(items) == type([]) and items[0] == '请输入管理员密码':
                self.denglu(browser)
            if browser.page_source.find('name="mainFrame"') == -1:
                # 写入数据库
                insert_data = {
                    "ip_address": '',
                    "status":0,
                    "insert_time":time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),
                    "executer":"本地网关,方法名 get_ip_source_one",
                    "beizhu":"解析网页时没有找到mainFrame这个节点"
                }
                ip_chuli(data=insert_data, session=self.session)
                return None
            result_ip = self.click_yunxing_status(browser)
            browser.quit()
            insert_data = {
                "ip_address": result_ip,
                "status": 1,
                "insert_time": time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),
                "executer": "本地网关,方法名 get_ip_source_one",
                "beizhu": "解析成功"
            }
            ip_chuli(data=insert_data, session=self.session)
            return result_ip
        except:
            traceback.print_exc()
            insert_data = {
                "ip_address": "",
                "status": 0,
                "insert_time": time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),
                "executer": "本地网关,方法名 get_ip_source_one",
                "beizhu": "解析异常出现报错"
            }
            ip_chuli(data=insert_data,session=self.session)

            println("访问chrome访问异常.该方法略过执行其他方法来获取ip地址")
            return None
        finally:
            self.session.close()
    def denglu(self,browser):
        browser.find_element_by_id('pcPassword').send_keys('xiaojian5791041')
        browser.find_element_by_id('loginBtn').click()
        return browser
    def click_yunxing_status(self,browser):
        browser.switch_to.frame("bottomLeftFrame")
        browser.find_element_by_id('a0').click()
        browser.switch_to_default_content()
        browser.switch_to.frame("mainFrame")
        pattern = re.compile(r'.*?<td>IP地址：</td><td>(.*?)</td>.*?')
        result_ip = re.findall(pattern,browser.page_source)
        if result_ip[0] == '0.0.0.0' or result_ip[0] == '127.0.0.1':
            # 写入数据库
            insert_data = {
                "ip_address":result_ip[0],
                "status": 0,
                "insert_time": time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),
                "executer": "本地网关,方法名 get_ip_source_one",
                "beizhu": "解析的地址不正确"
            }
            ip_chuli(data=insert_data, session=self.session)
            return None
        return result_ip[0]
    def db_save_data(self,data={}):
        """
        保存数据到数据库中
        :return:
        """
        self.session.add(get_ip_data_mode(data))
        self.session.commit()


class get_ip_source_two(get_ip_base):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.session = DBSession()
    """
    获取ip的第二种方法
    """
    def db_save_data(self,data={}):
        """
        保存数据到数据库中
        :return:
        """
        self.session.add(get_ip_data_mode(data))
        self.session.commit()
    def get_ip(self):
        """
        获取ip地址
        :return:
        """
        try:
            str = requests.get('https://ip.cn', timeout=5).text
            pattern = re.compile('Your IP</span>:(.*?)</span>', re.S)
            items = re.findall(pattern, str)
            content = items[0].strip()
            if content !='':
                insert_data = {
                    "ip_address": content,
                    "status": 1,
                    "insert_time": time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),
                    "executer": "网络获取,方法名 get_ip_source_two",
                    "beizhu": "解析成功"
                }
                ip_chuli(data=insert_data, session=self.session)
                return content
            else:
                insert_data = {
                    "ip_address": "",
                    "status": 0,
                    "insert_time": time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),
                    "executer": "网络获取,方法名 get_ip_source_two",
                    "beizhu": "解析失败"
                }
                ip_chuli(data=insert_data, session=self.session)
                return None
        except:
            insert_data = {
                "ip_address": "",
                "status": 0,
                "insert_time": time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),
                "executer": "网络获取,方法名 get_ip_source_two",
                "beizhu": "解析异常，程序发生错误"
            }
            ip_chuli(data=insert_data, session=self.session)
            traceback.print_exc()
            return None
        finally:
            self.session.close()

