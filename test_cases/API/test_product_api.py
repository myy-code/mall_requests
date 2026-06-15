"""商品管理核心业务流测试 (PmsProductController)
设计方法: 等价类划分 + 边界值分析 + 场景法
"""
import allure
import pytest

from utils.data_loader import load_yaml_data
from utils.logger import logger
from operation.product_op import (
    create_product, list_product, simple_search_product, batch_update_product
)

create_cases = load_yaml_data("product_data/product_test_data.yaml", key="create_cases")
list_cases = load_yaml_data("product_data/product_test_data.yaml", key="list_cases")
simple_list_cases = load_yaml_data("product_data/product_test_data.yaml", key="simple_list_cases")
batch_cases = load_yaml_data("product_data/product_test_data.yaml", key="batch_cases")


@allure.feature("商品管理")
class TestProduct:

    @allure.story("创建商品")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", create_cases,
                             ids=[c["id"] for c in create_cases])
    @pytest.mark.p0
    @pytest.mark.smoke
    def test_01_create_product(self, authed_product_api, case):
        result = create_product(authed_product_api, **case["body"])
        assert result.code == case["expected_code"], \
            f"预期 {case['expected_code']}，实际 {result.code}"
        if result.code == 200:
            assert result.success
            logger.info(f"✅ 创建成功")

    @allure.story("查询商品")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", list_cases,
                             ids=[c["id"] for c in list_cases])
    @pytest.mark.p0
    @pytest.mark.smoke
    def test_02_list_product(self, authed_product_api, case):
        result = list_product(authed_product_api, **case["params"])
        assert result.code == case["expected_code"]

        checks = case.get("checks", {})
        total = (result.data or {}).get("total", 0)
        page_list = (result.data or {}).get("list", [])

        if checks.get("total_gt"):
            assert total > 0, f"期望 total>0, 实际 {total}"
        if checks.get("total_eq") is not None:
            assert total == checks["total_eq"]
        if checks.get("list_empty"):
            assert len(page_list) == 0
        logger.info(f"✅ 查询成功: total={total}")

    @allure.story("模糊搜索")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", simple_list_cases,
                             ids=[c["id"] for c in simple_list_cases])
    @pytest.mark.p1
    def test_03_simple_list(self, authed_product_api, case):
        result = simple_search_product(
            authed_product_api, keyword=case.get("keyword")
        )
        assert result.code == case["expected_code"]

    @allure.story("批量操作")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", batch_cases,
                             ids=[c["id"] for c in batch_cases])
    @pytest.mark.p1
    def test_04_batch_operation(self, authed_product_api, case):
        result = batch_update_product(
            authed_product_api, action=case["action"],
            ids=case["ids"], **{case["action"]: case["value"]}
        )
        assert result.code == case["expected_code"]
