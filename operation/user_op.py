
from core.result_base import ResultBase
from utils.logger import logger




# 登陆接口
def login_user(username,password,user_api):
    result = ResultBase()
    res=user_api.login(
        json={
            "username": username,
            "password": password
        }
    )

    data=res.json()

    if data.get("code") == 200:
        result.success = True
        result.token = data.get("data", {}).get("token")
        result.msg = data.get("message", "")
    else:
        result.success = False
        result.error = f"登录失败: code={data.get('code')}, msg={data.get('message')}"

    result.response = res
    result.code=data.get("code")
    logger.info(f"登录结果: success={result.success}")
    return result

# 注册

def register_user(username,password,nickName,email,user_api,db=None):
    result=ResultBase()
    res=user_api.register(
        json={
            "username" : username,
            "password" : password,
            "nickName" : nickName,
            "email"    : email
        }
    )
    data=res.json()
    if data.get("code") == 200:
        result.success = True
        result.msg = data.get("message", "")
        # 数据库校验（可选，没传 db 时不校验）
        if db:
            user = db.query_one(
                "SELECT * FROM ums_admin WHERE username = %s",
                (username,)
            )
            if user and user['nick_name'] == nickName and user['email'] == email:
                logger.info(f"✅ 注册成功且数据库验证通过: 用户ID={user.get('id')}")
            else:
                logger.warning(f"⚠️ 数据库验证不通过")
        else:
            logger.info("✅ 注册成功（未做数据库校验）")
    else:
        result.success=False
        result.error=f"⚠️ 注册失败（预期）: code={data.get('code')},msg={data.get('message')}"
        logger.info(f"⚠️ 注册失败（预期）: {data.get('message')}")

    result.response = res
    result.code = data.get("code")
    logger.info(f"注册结果: success={result.success}")
    return result


# 刷新 token
def refresh_token(api):
    result = ResultBase()
    res = api.refreshToken()
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 登出
def logout_user(api):
    result = ResultBase()
    res = api.logout()
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 获取当前用户信息
def get_current_user_info(api):
    result = ResultBase()
    res = api.info()
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 分页查询用户列表
def list_users(api, **kwargs):
    result = ResultBase()
    res = api.list(params=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.data = data.get("data", {})
    result.response = res
    return result


# 获取指定用户
def get_user(api, **kwargs):
    result = ResultBase()
    res = api.get_user(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 修改用户信息
def update_user(api, **kwargs):
    result = ResultBase()
    res = api.update_user(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 修改密码
def update_password(api, **kwargs):
    result = ResultBase()
    res = api.updatePassword(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 修改用户状态
def update_user_status(api, **kwargs):
    result = ResultBase()
    res = api.update_status(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 删除用户
def delete_user(api, **kwargs):
    result = ResultBase()
    res = api.delete_user(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 分配角色
def assign_roles(api, **kwargs):
    result = ResultBase()
    res = api.roleUpdate(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


# 获取用户角色
def get_user_roles(api, **kwargs):
    result = ResultBase()
    res = api.roleUser(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result
