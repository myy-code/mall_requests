"""后台订单管理 API (OmsOrderController)"""
from api import BaseAPI


class OrderAdminAPI(BaseAPI):

    def list(self, **kwargs):
        return self.get(url="/order/list", **kwargs)

    def batch_delivery(self, **kwargs):
        return self.post(url="/order/update/delivery", **kwargs)

    def batch_close(self, **kwargs):
        return self.post(url="/order/update/close", **kwargs)

    def batch_delete(self, **kwargs):
        return self.post(url="/order/delete", **kwargs)

    def detail(self, **kwargs):
        return self.get(url=f"/order/{kwargs.pop('order_id')}", **kwargs)

    def update_receiver_info(self, **kwargs):
        return self.post(url="/order/update/receiverInfo", **kwargs)

    def update_money_info(self, **kwargs):
        return self.post(url="/order/update/moneyInfo", **kwargs)

    def update_note(self, **kwargs):
        return self.post(url="/order/update/note", **kwargs)
