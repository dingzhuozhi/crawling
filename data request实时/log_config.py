import logging
import os
from logging import handlers

"""
logging分级别，默认等级是warning，所以只有warning以上级别日志被打印出来，需要通过basicConfig进行配置
"""


def log(model_name):
    logger = logging.getLogger('test')
    logger.setLevel(level=logging.DEBUG)  # 定义输出级别

    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')  # 定义输出格式

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    if not os.path.exists("日志文件"):
        os.makedirs("日志文件")
    time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename=r'日志文件/{}.log'.format(model_name),
                                                                   when='D')
    time_rotating_file_handler.setLevel(logging.DEBUG)
    time_rotating_file_handler.setFormatter(formatter)

    logger.addHandler(time_rotating_file_handler)

    logger.addHandler(stream_handler)
    return logger
