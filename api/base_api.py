"""
BaseAPI：所有 API 类的基类
- 管理 Session 和 token
- 统一 get/post/put/delete 方法
"""
import logging

import requests



class BaseAPI:
    # 构造函数
    def __init__(self,base_url):
        # 项目根目录
        self.base_url=base_url
        self.session=requests.Session()

    # 获取TOKEN
    def set_token(self,token):
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}"
            }
        )



    # 统一http方法
    # get   param拼接在url上
    def get(self,url,**kwargs):
        return self.session.get(
            f"{self.base_url}{url}",
            **kwargs
        )

    # post  数据放在body
    # **kwargs可以接收多个参数
    # 例：
    # api.post("/login", json={"name": "admin"}, headers={"X-ID": "1"}, timeout=5)
    # # kwargs = {"json": {...}, "headers": {...}, "timeout": 5}
    # # session.post(url, json={...}, headers={...}, timeout=5)

    def post(self,url,**kwargs):
        return self.session.post(
            f"{self.base_url}{url}",
            **kwargs
        )


    #patch
    def patch(self,url,**kwargs):
        return self.session.patch(
            f"{self.base_url}{url}",
            **kwargs
        )



    # put
    def put(self, url, **kwargs):
        return self.session.put(
            f"{self.base_url}{url}",
            **kwargs
        )

    # delete
    def delete(self,url,**kwargs):
        return self.session.delete(
            f"{self.base_url}{url}",
            **kwargs
        )


