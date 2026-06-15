"""商品管理 API (PmsProductController)"""
from api import BaseAPI


class ProductAPI(BaseAPI):

    def create(self, **kwargs):
        return self.post(url="/product/create", **kwargs)

    def update_info(self, **kwargs):
        return self.get(url=f"/product/updateInfo/{kwargs.pop('product_id')}", **kwargs)

    def update(self, **kwargs):
        return self.post(url=f"/product/update/{kwargs.pop('product_id')}", **kwargs)

    def list(self, **kwargs):
        return self.get(url="/product/list", **kwargs)

    def simple_list(self, **kwargs):
        return self.get(url="/product/simpleList", **kwargs)

    def update_verify_status(self, **kwargs):
        return self.post(url="/product/update/verifyStatus", **kwargs)

    def update_publish_status(self, **kwargs):
        return self.post(url="/product/update/publishStatus", **kwargs)

    def update_recommend_status(self, **kwargs):
        return self.post(url="/product/update/recommendStatus", **kwargs)

    def update_new_status(self, **kwargs):
        return self.post(url="/product/update/newStatus", **kwargs)

    def update_delete_status(self, **kwargs):
        return self.post(url="/product/update/deleteStatus", **kwargs)
