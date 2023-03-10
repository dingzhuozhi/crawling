import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import undetected_chromedriver as uc
from datetime import datetime
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
                                                                   when='D')
    time_rotating_file_handler.setLevel(logging.DEBUG)
    time_rotating_file_handler.setFormatter(formatter)

    logger.addHandler(time_rotating_file_handler)

    logger.addHandler(stream_handler)
    return logger


logger = log("RNBZ")


def is_visible(driver, timeout=10):  # 等待元素出现
    try:
        ui.WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="coveo-result-list1"]/div/div[1]/a/h5/span')))
        return True
    except:
        return False


def main_1(title,
           website='https://www.rbnz.govt.nz/news-and-events/news#f:@hierarchicalz95xsz120xatopictagnames=[Monetary%20policy]'):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 无界面显示
    options.add_argument("--disable-gpu")  # 禁止gpu
    # options.add_argument("--disable-software-rasterizer")  # 无界面
    options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片
    options.add_argument("--disable-extensions")  # 禁用插件加载
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options, driver_executable_path='chromedriver.exe')  # 必须指定运行路径
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """  # 禁用webdriver
    })

    driver.get(website)
    count = 0
    while True:
        if count <= 20:
            if is_visible(driver, timeout=5):
                previous_text = driver.find_element(By.XPATH, '//*[@id="coveo-result-list1"]/div/div[1]/a/h5/span')
                previous_content = previous_text.text
            if previous_content == title:  # 如果首行标题仍为上次标题，则未更新，继续刷新
                print("waiting for data")
                count = count + 1
                time.sleep(random.randint(10, 15) / 1000)
            else:
                # new_text = driver.find_element(By.XPATH, '//*[@id="coveo-result-list1"]/div/div[1]/a')
                logger.info("标题更新")
                print(datetime.now())
                start = time.time()
                previous_text.click()
                main_text = driver.find_element(By.XPATH, '/html/body/div/div/main/div[3]/div/div').text

                send_udp("127.0.0.1", 32123, main_text)
                logger.info("{}".format(main_text))
                print(datetime.now())
                print(time.time() - start)
                # return main_text
        else:
            count = 0
            driver.refresh()
            time.sleep(random.randint(100, 150) / 1000)


if __name__ == '__main__':
    while datetime.now() < datetime(2023, 2, 21, 14,50,10):  # datetime(2023,2,22,8,59,50)
        time.sleep(1)
    print(datetime.now())
    logger.info("爬虫开始执行")
    previous_title = 'Monetary Policy Announcement and Financial Stability Report dates for 2023/24'
    main_1(previous_title)
