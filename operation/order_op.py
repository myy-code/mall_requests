from core.result_base import ResultBase
from utils.logger import logger


def list_order(api, **kwargs):
    result = ResultBase()
    res = api.list(params=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.data = data.get("data", {})
    result.response = res
    return result


def get_order_detail(api, **kwargs):
    result = ResultBase()
    res = api.detail(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"获取订单详情结果: code={result.code}")
    return result


def update_order_note(api, **kwargs):
    result = ResultBase()
    res = api.update_note(params=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"修改订单备注结果: code={result.code}")
    return result
