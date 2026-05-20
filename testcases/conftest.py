import logging
import os.path

import allure
import pytest
import yaml

from api import UserAPI, BaseAPI
from config.config import Settings
from utils.db_utils import DBUtils

"""获取token"""
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
    # FIX: .get("code",{}) 默认值 {} 类型错误，code 预期是数字，应改为 None 或 0
    # 避免 code 字段缺失时仍然继续执行导致后续 .json() 报错更难排查
    if data_json.get("code",None)!=200:
        pytest.fail(f"登陆失败:{data_json}")
    return data_json["data"]["token"]

# 设置session 请求头中的token
@pytest.fixture(scope="session")
def authed_api(token,setting):
    api=UserAPI(setting.base_url)
    api.set_token(token=token)
    return api


"""allure"""
# 在 item 上记录各阶段结果，供 allure_logs fixture 判断
# 标记这是一个钩子函数 tryfirst 在同类的钩子函数中优先执行  hookwrapper包装器钩子 包裹整个测试执行过程
@pytest.hookimpl(tryfirst=True,hookwrapper=True)
# 官方定义的标准运行时的钩子   item 代表正在执行的测试用例对象  call代表，当前执行阶段的对象  分为setup call teardown
def pytest_runtest_makereport(item, call):
    outcome=yield
    # 给对象添加一个属性
    # call.when：当前执行阶段的名称，只能是三个固定值：
    # "setup"：前置  fixture 执行阶段 # "call"
    # get_result()返回一个TestReport对象
    setattr(item,"rep_"+call.when,outcome.get_result())


# pytest_runtest_setup:  开始 setup 阶段 → 创建 handler → 存 caplog_records["setup"] = ...
# pytest_runtest_call:   开始 call 阶段  → 创建新 handler（旧清空）→ 存 caplog_records["call"] = ...
# pytest_runtest_teardown:开始 teardown 阶段 → 创建新 handler（旧清空）→ 存 caplog_records["teardown"] = ...
#                         ↓ 在此阶段执行 fixture 的 teardown（yield 之后的部分）
#                         此时 caplog.handler = teardown 阶段的 handler（空的）
# 简单说就是：测试的日志在 call 阶段，而你的 fixture 在 teardown 阶段运行时，caplog.records 或 caplog.text 只能拿到 teardown 阶段的内容（几乎没有日志），所以 attach 的是空字符串。


# 使用方式：
#   rm -r reports/allure-results/*  清理旧的allure报告
#   allure serve reports/allure-results  启动allure网页
@pytest.fixture(autouse=True)           # autouse=True：自动执行，所有测试无需声明参数
def allure_logs(request, caplog):
    """
    功能：测试用例失败时，自动将日志附加到 Allure 报告中。

    执行时机：
      - yield 之前（前置代码）：每个测试用例执行前运行（setup 阶段前）
      - yield 之后（后置代码）：测试用例全部执行完毕后运行（teardown 阶段后）

    关键细节：
      - pytest 9.0.3 中，每个测试阶段（setup/call/teardown）
        都独立创建 handler 并重置 records
      - teardown 阶段 caplog.records 或 caplog.text 只能拿到 teardown 阶段的日志（几乎为空）
      - 必须用 caplog.get_records("call") 获取测试函数执行阶段的日志
    """
    # ── 前置代码（setup 阶段前执行）──
    # 让 caplog 捕获 DEBUG 及以上级别的日志
    caplog.set_level(logging.DEBUG)

    # 交出控制权，等待测试用例完整执行（setup → call → teardown）
    yield

    # ── 后置代码（teardown 阶段后执行）──
    # 判断测试函数的 call 阶段是否失败
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # 获取 call 阶段（测试函数执行阶段）的日志记录
        records = caplog.get_records("call")

        # 手动拼接日志文本，避免 caplog.text 可能携带的 ANSI 颜色码
        log_text = "\n".join(
            f"{r.levelname} {r.name}:{r.filename}:{r.lineno} {r.getMessage()}"
            for r in records
        )

        # 将日志作为文本附件添加到 Allure 报告中
        allure.attach(
            log_text,
            name="测试日志",
            attachment_type=allure.attachment_type.TEXT
        )



"""获取数据库连接"""
@pytest.fixture(scope="session")
def db(setting):
    # 建立数据库连接每个测试会话只创建一次
    db=DBUtils(
        host=setting.db_host,
        port=setting.db_port,
        user=setting.db_user,
        password=setting.db_password,
        database=setting.db_database
    )
    yield db
    db.close()

