"""品牌场景测试：创建 → 查询 → 修改 → 删除
验证品牌完整生命周期流程
"""
import allure
import pytest

from core.allure_steps import step_setup, step_teardown
from core.base_test import BaseTest
from operation.brand_op import (
    create_brand, list_brand, get_brand_detail, update_brand, delete_brand
)
from utils.logger import logger


@allure.epic("商城后台管理系统")
@allure.feature("场景测试-品牌管理")
class TestBrandScenario(BaseTest):

    @allure.story("品牌生命周期")
    @allure.title("创建品牌 → 查询 → 修改 → 删除完整流程")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.multiple
    @pytest.mark.p0
    def test_brand_create_query_update_delete(self, authed_brand_api):
        """场景：创建品牌 → 列表查询 → 详情查询 → 修改品牌 → 删除品牌"""
        brand_body = {
            "name": "auto_test_品牌生命周期",
            "firstLetter": "P",
            "sort": 0,
            "factoryStatus": 1,
            "showStatus": 1,
            "logo": "https://example.com/logo.png",
            "bigPic": "https://example.com/bigpic.png",
            "brandStory": "自动化测试品牌描述"
        }

        # Step 1: 创建品牌
        logger.info("--- Step 1: 创建品牌 ---")
        create_result = create_brand(authed_brand_api, **brand_body)
        assert create_result.code == 200, f"创建品牌失败: {create_result.error}"
        brand_id = (create_result.response.json().get("data") or {}).get("id")
        logger.info(f"✅ 品牌创建成功: brand_id={brand_id}")

        # Step 2: 列表查询
        logger.info("--- Step 2: 列表查询品牌 ---")
        list_result = list_brand(authed_brand_api, keyword="auto_test_品牌生命周期", pageSize=10, pageNum=1)
        assert list_result.code == 200
        logger.info(f"✅ 列表查询成功: total={(list_result.data or {}).get('total', 0)}")

        # Step 3: 详情查询
        logger.info("--- Step 3: 详情查询 ---")
        detail_result = get_brand_detail(authed_brand_api, brand_id=brand_id)
        assert detail_result.code == 200
        assert detail_result.success
        logger.info(f"✅ 详情查询成功")

        # Step 4: 修改品牌
        logger.info("--- Step 4: 修改品牌 ---")
        update_body = {"name": "auto_test_品牌生命周期_已修改"}
        update_result = update_brand(authed_brand_api, brand_id=brand_id, **update_body)
        assert update_result.code == 200, f"修改品牌失败: {update_result.error}"
        logger.info(f"✅ 品牌修改成功")

        # Step 5: 删除品牌
        logger.info("--- Step 5: 删除品牌 ---")
        delete_result = delete_brand(authed_brand_api, brand_id=brand_id)
        assert delete_result.code == 200, f"删除品牌失败: {delete_result.error}"
        logger.info(f"✅ 品牌生命周期流程完成")

    @allure.story("查询不存在的品牌")
    @allure.title("查询不存在品牌应返回异常")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.multiple
    @pytest.mark.negative
    @pytest.mark.p2
    def test_brand_query_not_exist(self, authed_brand_api):
        """场景：查询不存在的品牌ID"""
        result = get_brand_detail(authed_brand_api, brand_id=99999)
        assert result.code != 200, f"不存在品牌应返回非200, code={result.code}"
        logger.info(f"✅ 查询不存在品牌返回 code={result.code}")


if __name__ == '__main__':
    pytest.main([__file__, "-v", "--alluredir=reports/allure-results"])
