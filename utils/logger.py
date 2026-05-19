"""
日志模块：统一日志配置
- 控制台输出 INFO 级别
- 文件记录 DEBUG 级别
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logger(name="mall_test", log_dir="logs"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), log_dir)
    os.makedirs(log_dir, exist_ok=True)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)

    file_handler = TimedRotatingFileHandler(
        os.path.join(log_dir, "test.log"),
        when="midnight",
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
