"""
bank of canda
https://www.bankofcanada.ca/2022/10/fad-press-release-2022-10-26/ 格式比较固定
main_text = driver.find_element(By.CLASS_NAME, 'post-content')
加拿大有13小时时差，但是都是中国时间晚上，所以还是在同一天
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import socket
import logging
import os
from logging import handlers

def send_udp(host,port,message):
    """
    :param host:
    :param port:
    :param message:
    :return:
    爬虫发送至指定端口，一般发到 127.0.0.1
    """
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.sendto(message.encode('utf-8'),(host,port))


def log(model_name):
    logger = logging.getLogger('test')
    logger.setLevel(level=logging.DEBUG)  # 定义输出级别
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')  # 定义输出格式
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    if not os.path.exists("爬虫日志文件"):
        os.makedirs("爬虫日志文件")
    time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename=r'爬虫日志文件/{}.log'.format(model_name),
                                                                   when='D',encoding="utf-8")
    time_rotating_file_handler.setLevel(logging.DEBUG)
    time_rotating_file_handler.setFormatter(formatter)
    logger.addHandler(time_rotating_file_handler)
    logger.addHandler(stream_handler)
    return logger


logger = log("BOC")

def main(website):
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.add_argument("--headless")  # 无界面显示
    options.add_argument("--disable-gpu")  # 禁止gpu
    options.add_argument("--disable-software-rasterizer")  # 无界面
    options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片
    options.add_argument("--disable-extensions")  # 禁用插件加载
    driver = webdriver.Chrome(options=options)
    driver.get(website)
    count = 0
    while True:
        if count <= 20:
            try:
                time.sleep(random.randint(100, 150) / 1000)
                error_text = driver.find_element(By.XPATH, '//*[@id="error_content"]/h1').text  # 如果文章出来了是没有error_text的
            except:
                error_text = "find it"
            if (error_text == '404 - file not found'):  # 则为未更新的页面或者不存在的页面
                logger.info("waiting for data")
                count = count + 1
                time.sleep(random.randint(10, 15) / 1000)
            else:
                try:
                    main_text = driver.find_element(By.CLASS_NAME, 'post-content')
                    if len(main_text.text) > 1000:  # 增加判断条件防止爬取错误内容
                        send_udp("127.0.0.1", 32123, main_text.text) #发送信号
                        logger.info("标题更新")
                        logger.info("{}".format(main_text.text))
                        return main_text.text
                    else:
                        logger.info("文本长度为{}".format(len(main_text.text)))
                        logger.info("小于1000字的文本为：{}".format(main_text.text))
                        pass
                except:
                    pass
        else:
            count = 0
            driver.refresh()
            time.sleep(random.randint(10, 15) / 1000)


if __name__ == '__main__':
    # date = "2023-01-25"
    date = "2023-03-08"
    website = "https://www.bankofcanada.ca/{}/{}/fad-press-release-{}/".format(date[:4], date[5:7], date)
    print(website)
    main(website)

