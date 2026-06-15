"""品牌管理 API (PmsBrandController)"""
from api import BaseAPI


class BrandAPI(BaseAPI):

    def list_all(self):
        return self.get(url="/brand/listAll")

    def create(self, **kwargs):
        return self.post(url="/brand/create", **kwargs)

    def update(self, **kwargs):
        return self.post(url=f"/brand/update/{kwargs.pop('brand_id')}", **kwargs)

    def delete(self, **kwargs):
        return self.get(url=f"/brand/delete/{kwargs.pop('brand_id')}", **kwargs)

    def list(self, **kwargs):
        return self.get(url="/brand/list", **kwargs)

    def get_detail(self, **kwargs):
        return self.get(url=f"/brand/{kwargs.pop('brand_id')}", **kwargs)

    def batch_delete(self, **kwargs):
        return self.post(url="/brand/delete/batch", **kwargs)

    def update_show_status(self, **kwargs):
        return self.post(url="/brand/update/showStatus", **kwargs)

    def update_factory_status(self, **kwargs):
        return self.post(url="/brand/update/factoryStatus", **kwargs)
