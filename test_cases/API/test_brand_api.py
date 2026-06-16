"""品牌管理核心业务流测试 (PmsBrandController)
设计方法: 等价类划分 + 边界值分析 + 错误推断
"""
import allure
import pytest

from utils.data_loader import load_yaml_data
from utils.logger import logger
from operation.brand_op import (
    create_brand, list_brand, get_brand_detail,
    update_brand, delete_brand, batch_update_brand_status
)

create_cases = load_yaml_data("brand_data/brand_test_data.yaml", key="create_cases")
list_cases = load_yaml_data("brand_data/brand_test_data.yaml", key="list_cases")
update_cases = load_yaml_data("brand_data/brand_test_data.yaml", key="update_cases")
delete_cases = load_yaml_data("brand_data/brand_test_data.yaml", key="delete_cases")
batch_cases = load_yaml_data("brand_data/brand_test_data.yaml", key="batch_status_cases")


@allure.epic("商城后台管理系统")
@allure.feature("品牌管理")
class TestBrand:

    @allure.story("创建品牌")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", create_cases,
                             ids=[c["id"] for c in create_cases])
    @pytest.mark.p0
    @pytest.mark.smoke
    def test_01_create_brand(self, authed_brand_api, case):
        result = create_brand(authed_brand_api, **case["body"])
        assert result.code == case["expected_code"], result.error
        if result.code == 200:
            assert result.success

    @allure.story("查询品牌")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", list_cases,
                             ids=[c["id"] for c in list_cases])
    @pytest.mark.p0
    @pytest.mark.smoke
    def test_02_list_brand(self, authed_brand_api, case):
        result = list_brand(authed_brand_api, **case["params"])
        assert result.code == case["expected_code"]

    @allure.story("查询品牌")
    @allure.title("获取品牌详情")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_03_get_brand_detail(self, authed_brand_api):
        result = get_brand_detail(authed_brand_api, brand_id=1)
        assert result.code == 200
        assert result.success

    @allure.story("查询品牌")
    @allure.title("获取不存在的品牌详情")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p2
    def test_04_get_brand_not_found(self, authed_brand_api):
        result = get_brand_detail(authed_brand_api, brand_id=99999)
        assert result.code in (200, 404)

    @allure.story("修改品牌")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", update_cases,
                             ids=[c["id"] for c in update_cases])
    @pytest.mark.p1
    def test_05_update_brand(self, authed_brand_api, case):
        result = update_brand(authed_brand_api, brand_id=case["brand_id"], **case["body"])
        assert result.code == case["expected_code"]

    @allure.story("删除品牌")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", delete_cases,
                             ids=[c["id"] for c in delete_cases])
    @pytest.mark.p1
    def test_06_delete_brand(self, authed_brand_api, case):
        result = delete_brand(authed_brand_api, brand_id=case["brand_id"])
        assert result.code == case["expected_code"]

    @allure.story("批量操作")
    @allure.title("{case[description]}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", batch_cases,
                             ids=[c["id"] for c in batch_cases])
    @pytest.mark.p1
    def test_07_batch_status(self, authed_brand_api, case):
        result = batch_update_brand_status(
            authed_brand_api, ids=case["ids"], showStatus=case["showStatus"]
        )
        assert result.code == case["expected_code"]


if __name__ == '__main__':
    pytest.main([__file__, "-v", "--alluredir=reports/allure-results"])
