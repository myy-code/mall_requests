import json
import os




class Settings:
    def __init__(self,env="test"):
        # 获取配置文件的文件地址
        config_file=os.path.join(os.path.dirname(__file__),"env_local.json")
        # 只读打开文件读取数据
        with open(config_file,"r",encoding="utf-8") as f:
            # 设置一个私有变量，存储文件中的数据
            self._config_data=json.load(f).get(env,{})


    # 只读方法
    @property
    def base_url(self):
        return self._config_data.get("base_url",{})

    @property
    def username(self):
        return self._config_data.get("username",{})

    @property
    def password(self):
        return self._config_data.get("password",{})

