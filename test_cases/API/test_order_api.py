"""后台订单管理测试 (OmsOrderController)
运行条件：mall-admin 服务运行中（端口 8080）
"""
import allure
import pytest

from utils.logger import logger
from operation.order_op import list_order, get_order_detail, update_order_note


@allure.epic("商城后台管理系统")
@allure.feature("订单管理-后台")
class TestOrderAdmin:

    @allure.story("后台查询")
    @allure.title("分页查询订单")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_01_admin_list(self, authed_order_admin_api):
        result = list_order(authed_order_admin_api, pageNum=1, pageSize=10)
        assert result.code == 200
        logger.info(f"✅ 后台订单查询成功")

    @allure.story("后台查询")
    @allure.title("订单详情查询")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_02_admin_detail(self, authed_order_admin_api):
        list_res = list_order(authed_order_admin_api, pageNum=1, pageSize=1)
        orders = (list_res.data or {}).get("list", [])
        if not orders:
            pytest.skip("无订单数据")
        order_id = orders[0].get("id")
        result = get_order_detail(authed_order_admin_api, order_id=order_id)
        assert result.code == 200
        assert result.success
        logger.info(f"✅ 订单详情获取成功: orderId={order_id}")

    @allure.story("后台操作")
    @allure.title("修改订单备注")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_03_update_note(self, authed_order_admin_api):
        list_res = list_order(authed_order_admin_api, pageNum=1, pageSize=1)
        orders = (list_res.data or {}).get("list", [])
        if not orders:
            pytest.skip("无订单数据")
        order_id = orders[0].get("id")
        result = update_order_note(
            authed_order_admin_api,
            id=order_id, note="自动化测试备注", status=0
        )
        assert result.code == 200
        logger.info(f"✅ 订单备注修改成功: orderId={order_id}")


if __name__ == '__main__':
    pytest.main([__file__, "-v", "--alluredir=reports/allure-results"])
