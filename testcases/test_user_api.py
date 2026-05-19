import pytest

from api import UserAPI



class TestUserLogin:

    # 验证是否登陆成功token是否已经设置在请求头里面了
    # 使用pytest.mark对测试用例进行标记   注：需要先创建一个pytest.ini文件用于注册标记
    # [pytest]
    # markers =
    # p0: 冒烟测试（核心流程，失败则阻断发布）
    # p1: 重要功能（常规回归必测）
    # p2: 边缘场景（异常分支、边界值）
    # smoke: 冒烟标签
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_login_success(self,authed_api):
        res=authed_api.info()
        assert res.status_code == 200

    # 注册
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_register(self,authed_api):
        res=authed_api.register(username="qwer",password="123456",nickName="伍六七",email="694932667@qq.com")
        assert res.status_code == 200
        print(res.json())

    # 刷新token
    @pytest.mark.p2
    def test_token(self,authed_api):
        res=authed_api.refreshToken()
        assert res.status_code == 200
        print(res.json())

    # 登出
    @pytest.mark.p0
    @pytest.mark.smoke
    def test_loginOut(self,authed_api):
        res=authed_api.logout()
        assert res.status_code == 200
        print(res.json())

    # 分页获取用户列表
    @pytest.mark.p1
    def test_list(self,authed_api):
        res=authed_api.list("伍六七",pagesize=5,pageNum=1)
        assert res.status_code == 200
        print(res.json())

    # 获取指定用户的信息
    @pytest.mark.p1
    def test_get_user(self,authed_api):
        res=authed_api.get_user(1)
        assert res.status_code == 200
        print(res.json())


    # 修改指定用户信息
    @pytest.mark.p1
    def test_update_user(self, authed_api):
        res = authed_api.update_user(
            user_id=1,
            username="admin",
            email="newemail@example.com",
            nickname="超级管理员",
            note="备注信息",
            status=1
        )
        assert res.status_code == 200
        print(res.json())

    # 修改密码
    @pytest.mark.p1
    def test_update_password(self, authed_api):
        res = authed_api.updatePassword(
            username="admin",
            oldPassword="macro123",
            newPassword="123456"
        )

        print(res.json())

    # 修改用户状态
    @pytest.mark.p1
    def test_update_user_status(self, authed_api):
        res = authed_api.update_status(user_id=1, status=1)
        assert res.status_code == 200
        print(res.json())

    # 删除用户
    @pytest.mark.p2
    def test_delete_user(self, authed_api):
        # 注意：删除操作需谨慎，建议使用测试账号
        res = authed_api.delete_user(user_id=11)
        assert res.status_code == 200
        data=res.json()
        assert data["code"] == 200 ,f"删除用户失败: {data.get('message')}"
        print(data)

    # 给用户分配角色
    @pytest.mark.p1
    def test_assign_roles(self, authed_api):
        res = authed_api.roleUpdate(admin_id=1, role_ids=[1, 2])
        assert res.status_code == 200
        print(res.json())

    # 获取指定用户的角色
    @pytest.mark.p1
    def test_get_user_roles(self, authed_api):
        res = authed_api.roleUser(admin_id=1)
        assert res.status_code == 200
        print(res.json())


