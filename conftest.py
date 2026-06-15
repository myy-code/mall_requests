import os
import shutil
import pytest
import logging
import allure
import pytest
import yaml
from api import UserAPI, BaseAPI, ProductAPI, BrandAPI, OrderAdminAPI
from config.config import Settings
from utils.data_loader import load_yaml_data
from utils.db_utils import DBUtils
from utils.logger import logger


def pytest_configure(config):
    # 确保 allure 报告输出到项目根目录下的 reports/
    # 不管从哪个目录运行 pytest，都不会在 test_cases/ 下生成 reports/
    if config.option.allure_report_dir:
        config.option.allure_report_dir = str(
            config.rootpath / config.option.allure_report_dir
        )





