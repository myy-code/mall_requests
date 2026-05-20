import json
import os

import yaml


class Settings:
    def __init__(self,env="test"):
        # 获取配置文件的文件地址
        config_file=os.path.join(os.path.dirname(__file__),"env_local.yaml")
        # 只读打开文件读取数据
        with open(config_file,"r",encoding="utf-8") as f:
            # 设置一个私有变量，存储文件中的数据
            self._config_data=yaml.safe_load(f).get(env,{})


    # 只读方法
    @property
    def base_url(self):
        # 拼接url时不能用{}会保存 使用空""
        return self._config_data.get("base_url","")

    # FIX: .get("username",{}) 返回空字典 {}，调用方使用时可能触发 TypeError
    # 应改为 .get("username","") 返回空字符串，和其他属性保持一致
    @property
    def username(self):
        return self._config_data.get("username","")

    # FIX: 同上，应改为 .get("password","")
    @property
    def password(self):
        return self._config_data.get("password","")

    # 获取数据库的信息
    @property
    def db_host(self):
        return self._config_data.get("db_host","")

    @property
    def db_port(self):
        # pymysql.connect() 要求 port 为 int 类型
        return int(self._config_data.get("db_port", 3307))

    @property
    def db_user(self):
        return self._config_data.get("db_user", "")

    @property
    def db_password(self):
        return self._config_data.get("db_password", "")

    @property
    def db_database(self):
        return self._config_data.get("db_database", "")

