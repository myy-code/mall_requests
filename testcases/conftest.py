import pytest

from api import UserAPI, BaseAPI
from config.config import Settings


# 实例化配置文件
@pytest.fixture(scope="session")
def setting():
    return Settings(env="test")

# 调用API的构造函数，将配置文件中的网页地址取出
@pytest.fixture(scope="session")
def user_api(setting):
    return UserAPI(setting.base_url)

# 获取token
@pytest.fixture(scope="session")
def token(setting,user_api):
    resp=user_api.login(setting.username,setting.password)
    data_json=resp.json()
    if data_json.get("code",{})!=200:
        pytest.fail(f"登陆失败:{data_json}")
    return data_json["data"]["token"]

# 设置session 请求头中的token
@pytest.fixture(scope="session")
def authed_api(token,setting):
    api=UserAPI(setting.base_url)
    api.set_token(token=token)
    return api



