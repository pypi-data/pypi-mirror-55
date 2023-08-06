from PythonZyjTools.DbConnect.db_config import envs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print("数据库链接地址："+envs['db_config'].SQLALCHEMY_DATABASE_URI)

# 连接中心
engine = create_engine(envs['db_config'].SQLALCHEMY_DATABASE_URI,echo=True)
# 数据库需要继承
DBSession = sessionmaker(bind=engine)
