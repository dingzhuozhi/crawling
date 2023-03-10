from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import random
import socket
from utils import send_udp

from log_config import log
logger=log("RBA")

def main(website):
    logger.info("爬取的网站url为:{}".format(website))
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
                main_text = driver.find_element(By.XPATH, '//*[@id="content"]').text  # 找到全文内容
                print(len(main_text))
            except:
                main_text = 'Page Not Found'
            if (main_text[4:18] == 'Page Not Found') or (len(main_text) < 1000):  # 则为未更新的页面或者不存在的页面
                print("waiting for data")
                count = count + 1
                time.sleep(random.randint(10, 15) / 1000)
            else:
                logger.info("文章已更新")
                logger.info("正文内容为:{}".format(main_text))
                # send_udp("127.0.0.1", 32123, main_text)
                return main_text

        else:
            count = 0
            driver.refresh()
            time.sleep(random.randint(10, 15) / 1000)


if __name__ == '__main__':
    website = "https://www.rba.gov.au/media-releases/2023/mr-23-07.html"  # 目前尚未得知最后的两位序号,需要2.7前得知

    print("crawl_website", ":", website)
    main(website)
