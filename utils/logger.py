import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logger(name="mall_test",log_dir=None,level=logging.DEBUG):
    # 返回一个logger实例 并指定名字
    logger=logging.getLogger(name)
    # 设置 logger的日志最低级别为debug
    logger.setLevel(level)
    # 如果存在直接返回
    if logger.handlers:
        return logger

    # 设置日志的格式
    fmt=logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H%M%S"
    )

    # 创建控制台handlers
    console=logging.StreamHandler()
    # IOFO为日志最低级别   循序为： logger的Level->handles的Level 经过两次筛选
    console.setLevel(logging.INFO)
    # 设置日志格式
    console.setFormatter(fmt)

    if log_dir is None:
        log_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"logs")

    os.makedirs(log_dir,exist_ok=True)
    #创建文件handlers
    file_handler=TimedRotatingFileHandler(
        os.path.join(log_dir,"test.log"),
        when="midnight",
        backupCount=7,
        encoding="utf-8"
    )
    # 设置file_handler的规则
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    # 将两个handler加入logger，日志会同时输出到控制台和文件中
    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

