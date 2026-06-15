from api import BaseAPI


class UserAPI(BaseAPI):

    def register(self, **kwargs):
        return self.post(url="/admin", **kwargs)

    def login(self, **kwargs):
        return self.post(url="/admin/session", **kwargs)

    def refreshToken(self):
        return self.post(url="/admin/token")

    def info(self):
        return self.get(url="/admin/me")

    def logout(self):
        return self.delete(url="/admin/session")

    def list(self, **kwargs):
        return self.get(url="/admin", **kwargs)

    def get_user(self, **kwargs):
        return self.get(url=f"/admin/{kwargs.pop('user_id')}", **kwargs)

    def update_user(self, **kwargs):
        return self.put(url=f"/admin/{kwargs.pop('user_id')}", **kwargs)

    def updatePassword(self, **kwargs):
        return self.put(url="/admin/password", **kwargs)

    def update_status(self, **kwargs):
        return self.patch(url=f"/admin/{kwargs.pop('user_id')}/status", **kwargs)

    def delete_user(self, **kwargs):
        return self.delete(url=f"/admin/{kwargs.pop('user_id')}", **kwargs)

    def roleUpdate(self, **kwargs):
        return self.put(url=f"/admin/{kwargs.pop('admin_id')}/roles", **kwargs)

    def roleUser(self, **kwargs):
        return self.get(url=f"/admin/{kwargs.pop('admin_id')}/roles", **kwargs)
