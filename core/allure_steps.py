"""
公共 Allure Step 函数
在 Allure 报告中以 Step 级别展示关键操作，提升报告可读性
"""
import allure


@allure.step("前置步骤：测试环境准备")
def step_setup():
    """测试前置准备步骤"""
    pass


@allure.step("后置步骤：测试环境清理")
def step_teardown():
    """测试后置清理步骤"""
    pass


@allure.step("管理员登录：用户名={username}")
def step_login(username):
    """管理员登录步骤"""
    pass


@allure.step("注册用户：用户名={username}, 昵称={nickName}")
def step_register(username, nickName):
    """用户注册步骤"""
    pass


@allure.step("调用接口：{api_desc}")
def step_api_call(api_desc):
    """通用接口调用步骤"""
    pass


@allure.step("断言验证：{assert_desc}")
def step_assert(assert_desc):
    """通用断言步骤"""
    pass


@allure.step("数据库验证：{db_desc}")
def step_db_check(db_desc):
    """数据库校验步骤"""
    pass


@allure.step("创建测试数据：{data_desc}")
def step_create_data(data_desc):
    """数据准备步骤"""
    pass


@allure.step("清理测试数据：{data_desc}")
def step_clean_data(data_desc):
    """数据清理步骤"""
    pass