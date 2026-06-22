import pytest
import allure

from api import UserAPI
from operation.user_op import (
    login_user, register_user, refresh_token, logout_user, get_current_user_info,
    list_users, get_user, update_user, update_password, update_user_status,
    delete_user, assign_roles, get_user_roles
)

from utils.data_loader import load_yaml_data, read_excel_test_cases
from utils.logger import logger


@allure.epic("商城后台管理系统")
class TestUserLogin:



    @allure.feature("用户认证")
    @allure.story("登录状态")
    @allure.title("登录成功后有token，能获取用户信息")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_01_login_success(self, authed_api):
        result = get_current_user_info(authed_api)
        assert result.code == 200
        assert result.success

    # 注册
    _register_cases = load_yaml_data("user_api_data/register_data.yaml", key="register_cases")
    @allure.feature("用户认证")
    @allure.story("注册")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "case",
        _register_cases,
        ids=[c.get("id", c["description"]) for c in _register_cases]
    )
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_02_register(self, authed_api, case, db, delete_register_user):
        res = register_user(
            username=case["username"],
            password=case["password"],
            nickName=case["nickName"],
            email=case["email"],
            user_api=authed_api,
            db=db
        )
        assert res.code == case["expected_code"]
        if res.code == 200:
            assert res.success
        else:
            assert not res.success

        # YAML 数据驱动
        # login_case=load_yaml_data("user_api_data/login_data.yaml", key="login_cases")
        # Excel 数据驱动

    login_case = read_excel_test_cases(
        "user_api_data/api_test_data.xlsx",
        sheet_name="登录测试数据",
        skiprows=0,
        required_columns=["username", "password"]
    )
    @allure.title("{case[description]}")
    @allure.feature("用户认证")
    @allure.story("登录")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize(
        "case",
        login_case,
        ids=[c.get("id", c["case_id"]) for c in login_case]
    )
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_03_login(self, user_api, case):
        res = login_user(case['username'], case['password'], user_api)
        assert res.code == int(case["expected_code"]), res.error

        if res.code == 200:
            assert res.success
        else:
            assert not res.success

    @allure.feature("用户认证")
    @allure.story("Token管理")
    @allure.title("刷新 token")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p2
    def test_04_token(self, authed_api):
        result = refresh_token(authed_api)
        assert result.code == 200
        assert result.success

    @allure.feature("用户认证")
    @allure.story("登录状态")
    @allure.title("登出成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    @pytest.mark.smoke
    def test_05_loginOut(self, authed_api):
        result = logout_user(authed_api)
        assert result.code == 200
        assert result.success

    @allure.feature("用户管理")
    @allure.story("查询")
    @allure.title("分页查询用户列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p1
    def test_06_list(self, authed_api):
        result = list_users(authed_api, keyword="伍六七", pagesize=5, pageNum=1)
        assert result.code == 200
        assert result.success

    @allure.feature("用户管理")
    @allure.story("查询")
    @allure.title("获取指定用户信息")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_07_get_user(self, authed_api):
        result = get_user(authed_api, user_id=1)
        assert result.code == 200
        assert result.success

    @allure.feature("用户管理")
    @allure.story("修改")
    @allure.title("修改用户信息")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_08_update_user(self, authed_api):
        result = update_user(
            authed_api,
            user_id=1,
            json={
                "username": "admin",
                "email": "newemail@example.com",
                "nickname": "超级管理员",
                "note": "备注信息",
                "status": 1
            }
        )
        assert result.code == 200
        assert result.success

    @allure.feature("用户管理")
    @allure.story("修改")
    @allure.title("修改密码")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p1
    def test_09_update_password(self, authed_api):
        result = update_password(
            authed_api,
            json={
                "username": "admin",
                "oldPassword": "macro123",
                "newPassword": "123456"
            }
        )
        assert result.success

    @allure.feature("用户管理")
    @allure.story("修改")
    @allure.title("修改用户状态")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_10_update_user_status(self, authed_api):
        result = update_user_status(authed_api, user_id=1, params={"status": 1})
        assert result.code == 200
        assert result.success

    @allure.feature("用户管理")
    @allure.story("删除")
    @allure.title("删除用户")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p2
    def test_11_delete_user(self, authed_api):
        result = delete_user(authed_api, user_id=11)
        assert result.code == 200
        assert result.success

    @allure.feature("用户管理")
    @allure.story("角色")
    @allure.title("给用户分配角色")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p1
    def test_12_assign_roles(self, authed_api):
        result = assign_roles(authed_api, admin_id=1, json=[1, 2])
        assert result.code == 200
        assert result.success

    @allure.feature("用户管理")
    @allure.story("角色")
    @allure.title("获取指定用户的角色")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_13_get_user_roles(self, authed_api):
        result = get_user_roles(authed_api, admin_id=1)
        assert result.code == 200
        assert result.success


if __name__ == '__main__':
    pytest.main([__file__, "-v", "--alluredir=reports/allure-results"])
