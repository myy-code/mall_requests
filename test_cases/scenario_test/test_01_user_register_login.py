"""用户场景测试：注册 → 登录 → 查看信息
验证完整用户生命周期流程
"""
import allure
import pytest

from core.allure_steps import step_setup, step_teardown, step_login, step_register
from core.base_test import BaseTest
from operation.user_op import (
    register_user, login_user, get_current_user_info, logout_user
)
from utils.logger import logger


@allure.epic("商城后台管理系统")
@allure.feature("场景测试-用户管理")
class TestUserScenario(BaseTest):

    @allure.story("注册登录完整流程")
    @allure.title("用户注册后登录并查看信息")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.multiple
    @pytest.mark.p0
    @pytest.mark.usefixtures("delete_register_user")
    def test_user_register_login_info(self, user_api, authed_api):
        """场景：注册新用户 → 用新用户登录 → 查看用户信息 → 登出"""
        test_user = {
            "username": "autotest_user",
            "password": "123456",
            "nickName": "自动化测试用户",
            "email": "autotest@test.com"
        }

        # Step 1: 注册
        logger.info("--- Step 1: 注册新用户 ---")
        reg_result = register_user(
            username=test_user["username"],
            password=test_user["password"],
            nickName=test_user["nickName"],
            email=test_user["email"],
            user_api=authed_api
        )
        self.assert_code(reg_result, 200, "注册新用户")

        # Step 2: 用新注册用户登录
        logger.info("--- Step 2: 新用户登录 ---")
        login_result = login_user(
            username=test_user["username"],
            password=test_user["password"],
            user_api=user_api
        )
        self.assert_code(login_result, 200, "新用户登录")
        assert login_result.token, "登录成功但未获取到 token"

        # Step 3: 登录后获取用户信息
        logger.info("--- Step 3: 获取用户信息 ---")
        new_user_api = type(user_api)(user_api.base_url)
        new_user_api.set_token(login_result.token)
        info_result = get_current_user_info(new_user_api)
        self.assert_code(info_result, 200)
        self.assert_success(info_result)
        logger.info(f"✅ 用户场景流程完成: {test_user['username']}")

        # Step 4: 登出
        logger.info("--- Step 4: 登出 ---")
        logout_result = logout_user(new_user_api)
        self.assert_code(logout_result, 200)

    @allure.story("重复注册校验")
    @allure.title("重复注册相同用户名应失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.multiple
    @pytest.mark.negative
    @pytest.mark.p1
    def test_user_duplicate_register(self, authed_api):
        """场景：第一次注册成功 → 第二次注册相同用户名应失败"""
        test_user = {
            "username": "autotest_dup",
            "password": "123456",
            "nickName": "重复注册测试",
            "email": "dup@test.com"
        }

        # 第一次注册
        logger.info("--- 第一次注册 ---")
        reg1 = register_user(
            username=test_user["username"],
            password=test_user["password"],
            nickName=test_user["nickName"],
            email=test_user["email"],
            user_api=authed_api
        )
        self.assert_code(reg1, 200, "第一次注册应成功")

        # 第二次注册（应失败）
        logger.info("--- 第二次注册（预期失败） ---")
        reg2 = register_user(
            username=test_user["username"],
            password=test_user["password"],
            nickName=test_user["nickName"],
            email=test_user["email"],
            user_api=authed_api
        )
        assert reg2.code != 200, f"重复注册应失败，但返回 code={reg2.code}"
        logger.info(f"✅ 重复注册校验通过: code={reg2.code}")


if __name__ == '__main__':
    pytest.main([__file__, "-v", "--alluredir=reports/allure-results"])
