from core.result_base import ResultBase
from utils.logger import logger


def create_product(api, **kwargs):
    result = ResultBase()
    res = api.create(json=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"创建商品结果: code={result.code}")
    return result


def list_product(api, **kwargs):
    result = ResultBase()
    res = api.list(params=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.data = data.get("data", {})
    result.response = res
    return result


def simple_search_product(api, **kwargs):
    result = ResultBase()
    res = api.simple_list(params=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    return result


def batch_update_product(api, action, **kwargs):
    result = ResultBase()
    action_map = {
        "publishStatus": api.update_publish_status,
        "recommendStatus": api.update_recommend_status,
        "newStatus": api.update_new_status,
        "deleteStatus": api.update_delete_status,
    }
    func = action_map.get(action)
    if not func:
        result.error = f"未知操作: {action}"
        return result

    res = func(params=kwargs)
    data = res.json()
    result.code = data.get("code")
    result.success = (result.code == 200)
    result.response = res
    logger.info(f"批量操作商品结果: action={action}, code={result.code}")
    return result
