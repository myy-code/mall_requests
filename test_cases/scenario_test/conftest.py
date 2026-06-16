"""场景测试专用 fixtures"""
import pytest

from utils.data_loader import load_yaml_data


@pytest.fixture(scope="function")
def scenario_data(request):
    """根据测试函数名自动加载对应的场景测试数据"""
    return load_yaml_data(
        "scenario_data/scenario_test_data.yaml",
        key=request.function.__name__
    )
