import os
def get_db_uri(dbinfo):
    """
    组合成连接数据库字符串
    :param dbinfo: 数据字典
    :return: 连接数据库字符串
    """
    ENGINE = dbinfo.get('ENGINE') or 'mysql'
    DRIVER = dbinfo.get('DRIVER') or 'pymysql'
    USER = dbinfo.get('USER')
    PASSWORD = dbinfo.get('PASSWORD')
    HOST = dbinfo.get('HOST') or '127.0.0.1'
    PORT = dbinfo.get('PORT') or '3306'
    DBNAME = dbinfo.get('DBNAME')
    return "{}+{}://{}:{}@{}:{}/{}".format(ENGINE,DRIVER,USER,PASSWORD,HOST,PORT,DBNAME)


class db_config():
    DATABASE ={
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'ceshi',
        'PASSWORD': 'ceshi',
        'HOST': '127.0.0.1',
        'PORT': '3307',
        'DBNAME':'rengwu'
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)

envs = {
    'db_config': db_config
}

