from core.result_base import ResultBase
from utils.logger import logger


def create_brand(api, **kwargs):
    result = ResultBase()
    res = api.create(json=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"创建品牌结果: code={result.code}")
    return result


def list_brand(api, **kwargs):
    result = ResultBase()
    res = api.list(params=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.data = data.get("data", {})
    result.response = res
    return result


def get_brand_detail(api, **kwargs):
    result = ResultBase()
    res = api.get_detail(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"获取品牌详情结果: code={result.code}")
    return result


def update_brand(api, **kwargs):
    result = ResultBase()
    brand_id = kwargs.pop("brand_id")
    res = api.update(brand_id=brand_id, json=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"修改品牌结果: code={result.code}")
    return result


def delete_brand(api, **kwargs):
    result = ResultBase()
    res = api.delete(**kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"删除品牌结果: code={result.code}")
    return result


def batch_update_brand_status(api, **kwargs):
    result = ResultBase()
    res = api.update_show_status(params=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"批量修改品牌状态结果: code={result.code}")
    return result
