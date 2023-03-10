from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import io
import sys
import pandas
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import time

def main(website):
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.add_argument("--headless")  # 无界面显示
    options.add_argument("--disable-gpu")  # 禁止gpu
    options.add_argument("--disable-software-rasterizer")  # 无界面
    options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片
    options.add_argument("--disable-extensions")  # 禁用插件加载
    driver = webdriver.Chrome(options=options)
    count = 0
    driver.get(website)  # 需要修改网址
    while True:
        if count <= 20:
            try:
                title = driver.find_element(By.XPATH, '//*[@id="content"]').text  # 找到全文内容
            except:
                title = "find it"
            if (title[5:19] == 'Page not found'):  # 则为未更新的页面或者不存在的页面
                print("waiting for data")
                count = count + 1
                time.sleep(random.randint(5, 10) / 1000)
            else:
                try:
                    print("find it")
                    main_text = driver.find_element(By.XPATH, '//*[@id="article"]')
                    return main_text.text
                except:
                    pass
        else:  # 未更新次数超过20，刷新网页
            driver.refresh()
            time.sleep(random.randint(10,15)/1000)
            count = 0  # 重新计时


if __name__ == '__main__':
    website="https://www.federalreserve.gov/monetarypolicy/fomcminutes20211215.htm"
    #website="https://www.federalreserve.gov/monetarypolicy/fomcminutes20230201.htm"
    print(main(website))
