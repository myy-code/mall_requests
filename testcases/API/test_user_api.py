import pytest
import allure

from api import UserAPI

from utils.data_loader import load_yaml_data, read_excel_test_cases
from utils.logger import logger


class TestUserLogin:

    # YAML 数据驱动
    # login_case=load_yaml_data("user_api_data/login_data.yaml", key="login_cases")
    # Excel 数据驱动
    login_case=read_excel_test_cases(
        "user_api_data/api_test_data.xlsx",
        sheet_name="登录测试数据",
        skiprows=0,
        required_columns=["username","password"]
    )
    @allure.title("{case[description]}")  # 从数据驱动中取值作为用例标题
    @allure.feature("用户认证")             # feature：模块名
    @allure.story("登录")                  # story：子功能
    @pytest.mark.parametrize(
        "case",
        login_case,
        ids=[c.get("id", c["case_id"]) for c in login_case]
    )
    @pytest.mark.smoke
    @pytest.mark.p0
    # FIX: 手动创建 UserAPI(setting.base_url) 和 fixture user_api 重复
    # 建议注入 user_api fixture 替代手动实例化，保持一致性
    def test_login(self,setting,case):
        user_api=UserAPI(setting.base_url)
        res=user_api.login(
            username=case["username"],
            password=case["password"]
        )
        assert res.json()["code"] == int(case["expected_code"])



    # 验证是否登陆成功token是否已经设置在请求头里面了
    # 一级功能模块分类
    @allure.feature("用户认证")
    # 二级子模块分类
    @allure.story("登录状态")
    # 单个测试用例的标题
    @allure.title("登录成功后有 token，能获取用户信息")
    # 测试用例的严重级别   BLOCKER   阻塞级、CRITICAL	严重级、NORMAL	普通级（默认）、MINOR	轻微级、TRIVIAL	琐碎级
    @allure.severity(allure.severity_level.BLOCKER)  # 阻塞级别
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_login_success(self,authed_api):
        res=authed_api.info()
        assert res.status_code == 200

    # 注册
    _register_cases = load_yaml_data("user_api_data/register_test_data.yaml", key="register_cases")
    @allure.feature("用户认证")
    @allure.story("注册")
    @allure.title("{case[description]}")
    @pytest.mark.parametrize(
        "case",
        _register_cases,
        ids=[c.get("id", c["description"]) for c in _register_cases]
    )
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_register(self, authed_api, case,db):
        res = authed_api.register(
            username=case["username"],
            password=case["password"],
            nickName=case["nickName"],
            email=case["email"]
        )
        assert res.json()["code"] == case["expected_code"]

        # 数据库的校验
        if res.json()["code"] == 200:
            user=db.query_one(
                "SELECT * FROM ums_admin WHERE username =%s",
                (case["username"])
            )


            assert user['nick_name'] == case["nickName"]
            assert user['email'] == case["email"]
            logger.info(f"✅ 注册成功且数据库验证通过: 用户ID={user.get('id')}")
        else:
            logger.info(f"⚠️ 注册失败（预期）: {res.json().get('message')}")


    # 刷新token
    @allure.feature("用户认证")
    @allure.story("Token管理")
    @allure.title("刷新 token")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p2
    def test_token(self,authed_api):
        res=authed_api.refreshToken()
        assert res.status_code == 200
        print(res.json())

    # 登出
    @allure.feature("用户认证")
    @allure.story("登录状态")
    @allure.title("登出成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    @pytest.mark.smoke
    def test_loginOut(self,authed_api):
        res=authed_api.logout()
        assert res.status_code == 200
        print(res.json())

    # 分页获取用户列表
    @allure.feature("用户管理")
    @allure.story("查询")
    @allure.title("分页查询用户列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p1
    def test_list(self,authed_api):
        res=authed_api.list("伍六七",pagesize=5,pageNum=1)
        assert res.status_code == 200
        print(res.json())

    # 获取指定用户的信息
    @allure.feature("用户管理")
    @allure.story("查询")
    @allure.title("获取指定用户信息")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_get_user(self,authed_api):
        res=authed_api.get_user(1)
        assert res.status_code == 200
        print(res.json())


    # 修改指定用户信息
    @allure.feature("用户管理")
    @allure.story("修改")
    @allure.title("修改用户信息")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_update_user(self, authed_api):
        res = authed_api.update_user(
            user_id=1,
            username="admin",
            email="newemail@example.com",
            nickname="超级管理员",
            note="备注信息",
            status=1
        )
        assert res.status_code == 200
        print(res.json())

    # 修改密码
    @allure.feature("用户管理")
    @allure.story("修改")
    @allure.title("修改密码")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p1
    def test_update_password(self, authed_api):
        res = authed_api.updatePassword(
            username="admin",
            oldPassword="macro123",
            newPassword="123456"
        )

        print(res.json())

    # 修改用户状态
    @allure.feature("用户管理")
    @allure.story("修改")
    @allure.title("修改用户状态")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_update_user_status(self, authed_api):
        res = authed_api.update_status(user_id=1, status=1)
        assert res.status_code == 200
        print(res.json())

    # 删除用户
    @allure.feature("用户管理")
    @allure.story("删除")
    @allure.title("删除用户")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p2
    def test_delete_user(self, authed_api):
        # 注意：删除操作需谨慎，建议使用测试账号
        res = authed_api.delete_user(user_id=11)
        assert res.status_code == 200
        data=res.json()
        assert data["code"] == 200 ,f"删除用户失败: {data.get('message')}"
        print(data)

    # 给用户分配角色
    @allure.feature("用户管理")
    @allure.story("角色")
    @allure.title("给用户分配角色")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p1
    def test_assign_roles(self, authed_api):
        res = authed_api.roleUpdate(admin_id=1, role_ids=[1, 2])
        assert res.status_code == 200
        print(res.json())

    # 获取指定用户的角色
    @allure.feature("用户管理")
    @allure.story("角色")
    @allure.title("获取指定用户的角色")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_get_user_roles(self, authed_api):
        res = authed_api.roleUser(admin_id=1)
        assert res.status_code == 200
        print(res.json())


