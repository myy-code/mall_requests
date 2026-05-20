import os
from typing import Dict, List, Optional

import pandas as pd
import yaml


def load_yaml_data(file_name, key=None):
    data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(data_dir, "data", file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    cases = data[key] if key else list(data.values())[0]
    return cases

# 读取excel文件
# 类型提示
def read_excel_test_cases(
        file_name : str,
        sheet_name : str,
        # 列名列表 Optional 这个参数可传入的类型
        required_columns :Optional[List[str]] =None,
        #跳过的行数，如果前两行为说明文字 则 为2
        skiprows : int=0,
        # 是否区分大小写
        case_sensitive_columns: bool = False
)->List[Dict]:
    # 输入参数的校验
    if not file_name or not isinstance(file_name,str):
        raise ValueError("参数file_name不能为空而且必须为字符串")
    if not sheet_name or not isinstance(sheet_name,str):
        raise ValueError("参数sheet_name不为空而且必须为字符串")

    if required_columns is None:
        required_columns=[]


    # 找到读取文件所在的路劲
    data_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_dir=os.path.join(data_dir,"data",file_name)

    # 读取excel文件
    try:
        # 使用pandas中的读取excel的函数
        df=pd.read_excel(
            file_dir,
            sheet_name=sheet_name,
            # 所有输出格式都为字符串
            dtype=str,
            skiprows=skiprows,
            # 指定 pandas 使用 openpyxl 库来读取 Excel 文件
            engine="openpyxl"
        )
    except FileExistsError:
        raise FileExistsError(f"测试用例文件不存在，请检测路径:{file_dir}")
    except ValueError as e:
        # 检查异常信息中是否包含 "Worksheet named" 这个字符串
        if "Worksheet named" in str(e):
            raise ValueError(
                f"Excel文件中不存在工作表：{sheet_name}，请检查工作表名称"
            ) from e
        raise ValueError(
            f"Excel文件格式错误：{str(e)}"
        ) from e
    except PermissionError:
        raise PermissionError(
            f"没有权限读取文件：{file_dir}，请关闭Excel后重试"
        )
    except ImportError:
        raise ImportError(
            "缺少读取xlsx文件的依赖，请执行：pip install openpyxl"
        )
    except Exception as e:
        raise Exception(
            f"读取Excel文件失败：{str(e)}"
        ) from e

    # 列名标准化处理
    df=df.rename(
        columns=lambda x:x.strip() if isinstance(x,str) else str(x)
    )

    # 检测是否有重复列名
    duplicate_columns= df.columns[df.columns.duplicated()].tolist()
    if duplicate_columns:
        raise ValueError(
            f"Excel中存在重复列名：{duplicate_columns}，请删除重复列"
        )

    # 判断必填列名校验
    missing_columns=[col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"需要的必填项为：{required_columns}"
            f"Excel缺少必填项:{missing_columns}"
            f"当前列名为：{df.columns}"
        )

    # 用例过滤
    # 过滤禁用的用例
    if "status" in df.columns:
        df=df[df["status"].str.strip().str.upper() !="N"]
    # 删除全为空值的行
    df = df.dropna(how="all")
    # 将空值统一替换成None dtype=str 空值为nan python识别不了会报错
    df=df.replace(["nan","Nan",pd.NA, pd.NaT],None)
    # 转换为字典格式 返回值为列表
    return df.to_dict(orient="records")
