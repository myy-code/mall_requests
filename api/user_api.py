from api import BaseAPI


class UserAPI(BaseAPI):
    # 用户注册
    def register(self,username,password,nickName,email):
        return self.post(
            url="/admin",
            json={
                "username": username,
                "password": password,
                "nickName": nickName,
                "email": email
            }
        )

    # 用户登陆
    def login(self,username,password):
        return self.post(
            url="/admin/session",
            json={
                "username":username,
                "password":password
            }
        )

    # 刷新token
    def refreshToken(self):
        return self.post(
            url="/admin/token"
        )

    # 获取当前登陆用户的信息
    def info(self):
        return self.get(
            url="/admin/me"
        )

    # 登出
    def logout(self):
        return self.delete(
            url="/admin/session"
        )

    # 分页获取用户列表
    def list(self,keyword=None,pagesize=5,pageNum=1):
        return self.get(
            url="/admin",
            params={
                "keyword":keyword,
                "pagesize":pagesize,
                "pageNum":pageNum
            }
        )

    # 获取指定用户信息
    def get_user(self,user_id):
        return self.get(
            url=f"/admin/{user_id}"
        )

    #修改指定用户的信息
    def update_user(self,user_id,username,email,nickname,note,status):
        return self.put(
            url=f"/admin/{user_id}",
            json={
                "username":username,
                "email":email,
                "nickname":nickname,
                "note":note,
                "status":status
            }
        )

    #修改密码
    def updatePassword(self,username,oldPassword,newPassword):
        return self.put(
            url="/admin/password",
            json={
                "username":username,
                "oldPassword":oldPassword,
                "newPassword":newPassword
            }
        )

    # 修改用户状态
    def update_status(self, user_id, status):
        return self.patch(
            url=f"/admin/{user_id}/status",
            params={"status": status}
        )

    # 删除用户
    def delete_user(self, user_id):
         return self.delete(
         url=f"/admin/{user_id}"
        )

    # 给用户分配角色
    def roleUpdate(self,admin_id,role_ids):
        return self.put(
            url=f"/admin/{admin_id}/roles",
            json=role_ids
        )

    # 获取指定用户的角色
    def roleUser(self,admin_id):
        return self.get(
            url=f"/admin/{admin_id}/roles"
        )