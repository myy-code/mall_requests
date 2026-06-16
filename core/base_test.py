"""
测试基类
提供测试用例的通用基础设施：日志标记、Allure step 集成
子类可选继承，不强制修改现有代码
"""
import allure
import pytest

from utils.logger import logger
from core.allure_steps import step_setup, step_teardown


class BaseTest:
    """API 测试基类

    使用方式（可选）:
        class TestXxx(BaseTest):
            ...
    """

    def setup_method(self):
        """每个测试方法执行前自动运行"""
        test_name = self._current_test_name()
        logger.info("=" * 60)
        logger.info(f"▶ 开始执行: {test_name}")
        step_setup()

    def teardown_method(self):
        """每个测试方法执行后自动运行"""
        test_name = self._current_test_name()
        step_teardown()
        logger.info(f"✓ 执行结束: {test_name}")
        logger.info("=" * 60)

    def _current_test_name(self) -> str:
        """获取当前测试方法名"""
        # pytest 运行时通过 request.node 获取，非 pytest 环境 fallback
        try:
            import inspect
            for frame_info in inspect.stack():
                if frame_info.function.startswith("test_"):
                    return frame_info.function
        except Exception:
            pass
        return self.__class__.__name__

    @staticmethod
    def assert_code(result, expected_code: int, msg: str = ""):
        """统一断言：验证接口返回 code"""
        assert result.code == expected_code, \
            f"{msg} 期望code={expected_code}, 实际code={result.code}, 错误={result.error}"

    @staticmethod
    def assert_success(result, expect_success: bool = True):
        """统一断言：验证操作是否成功"""
        assert result.success == expect_success, \
            f"期望success={expect_success}, 实际success={result.success}, 错误={result.error}"