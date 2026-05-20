"""
BaseAPI：所有 API 类的基类
- 管理 Session 和 token
- 统一 get/post/put/delete 方法
"""
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.logger import logger


class BaseAPI:
    # 构造函数
    def __init__(self,base_url):
        # 项目根目录
        self.base_url = base_url
        self.session = requests.Session()

        # 设置请求超时时间：连接超时5秒，读取超时15秒
        self.timeout = (5, 15)

        # 配置自动重试机制，处理临时性服务器错误
        retry=Retry(
            total=2,   # 最多重试2次
            backoff_factor=0.5,  # 重试间隔倍数：第1次等待0.5s，第2次等待1s
            status_forcelist=[500, 502, 503], # 仅对这些服务器错误状态码进行重试
        )

        # 创建 HTTP 适配器并挂载重试策略
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    # 获取TOKEN
    def set_token(self,token):
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}"
            }
        )

    # 添加日志功能
    def _request(self,method,url,**kwargs):
        # 1. 拼接完整的 URL
        full_url = f"{self.base_url}{url}"

        # 2. 记录请求日志（将 HTTP 方法转为大写）
        logger.info(f"{method.upper()} {full_url}")

        # 3. 记录开始时间（用于计算请求耗时）
        start = time.time()

        # 4. 发送 HTTP 请求（如果 kwargs 没传 timeout，就用默认的 self.timeout）
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        resp = self.session.request(method, full_url, **kwargs)

        # 5. 计算请求耗时
        cost = time.time() - start

        # 6. 记录响应状态码和耗时
        logger.info(f" {resp.status_code} ({cost:.3f}s)")

        # 7. 如果状态码 >= 400，记录错误响应内容（前300字符）
        if resp.status_code >= 400:
            logger.error(f"响应: {resp.text[:300]}")

        # 8. 返回响应对象
        return resp

    # 统一http方法
    def get(self,url,**kwargs):
        return self._request("get",url,**kwargs)

    def post(self,url,**kwargs):
        return self._request("post",url,**kwargs)

    def patch(self,url,**kwargs):
        return self._request("patch",url,**kwargs)

    def put(self, url, **kwargs):
        return self._request("put",url,**kwargs)

    def delete(self,url,**kwargs):
        return self._request("delete",url,**kwargs)








