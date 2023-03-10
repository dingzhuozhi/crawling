"""
european central bank 欧洲中央银行
ecb网站后缀无法预测，只能通过前置页面判断是否更新。
ecb持续时间短，会被反爬
ecb在更新前，历史内容会归到snippet1，新内容会是snippet0
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import undetected_chromedriver as uc
import io
import sys
from datetime import datetime
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

def main_2(website):  # 进入 monetary decisions 页面抓取文本
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.add_argument("--headless")  # 无界面显示
    options.add_argument("--disable-gpu")  # 禁止gpu
    options.add_argument("--disable-software-rasterizer")  # 无界面
    options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片
    options.add_argument("--disable-extensions")  # 禁用插件加载
    driver = webdriver.Chrome(options=options)
    driver.get(website)
    main_text = driver.find_element(By.XPATH, '//*[@id="main-wrapper"]/main/div[2]')
    return (main_text.text)


def main(date, website="https://www.ecb.europa.eu/press/govcdec/mopo/html/index.en.html"):  # 进入前置页面查询文本是否更新
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'normal'
    options.add_argument("--headless")  # 无界面显示
    options.add_argument("--disable-gpu")  # 禁止gpu
    options.add_argument("--disable-software-rasterizer")  # 无界面
    options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片
    options.add_argument("--disable-extensions")  # 禁用插件加载
    driver = uc.Chrome(options=options)
    driver.get(website)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """  # 禁用webdriver
    })
    use_cookie = driver.find_element(By.XPATH, '//*[@id="cookieConsent"]/div[1]/div/a[2]')  # 点击cookie块
    use_cookie.click()
    time.sleep(1)
    count = 0
    while True:
        if count <= 20:
            try:
                first_catch = driver.find_element(By.XPATH, '//*[@id="snippet0"]/dt[1]/div').text  # 定位snippet0的内容块，
            except:
                first_catch = "not renew "
                print("not renew")
            if (first_catch != date):  # 则为未更新的页面或者不存在的页面
                print("waiting for data")
                count = count + 1
                time.sleep(random.randint(10, 15) / 1000)
            else:
                try:
                    href_catch = driver.find_element(By.XPATH, '//*[@id="snippet0"]/dd[1]/div[1]/a')  # 定位后置文本网页的href
                    website = href_catch.get_attribute("href")
                    main_text = main_2(website)
                    print(main_text)
                    return main_text
                except:
                    pass
        else:
            count = 0
            driver.refresh()
            time.sleep(random.randint(100, 150) / 1000)


if __name__ == '__main__':
    while True:
        try:
            print(main(date="2 February 2023"))
        except:
            print("报错，重新获取")

    # try:
    #     print(main(date="2 February 2023"))  # 2023.2.2ECB爬虫
    # except:
    #     print(datetime.now())  #
    #     print(time.time() - start)  # 经过多久运行错误
    #     print(main(date="2 February 2023"))

    # https://www.ecb.europa.eu/press/pr/date/2022/html/ecb.mp221027~df1d778b84.en.html

# TODO
# 运行时间久了会报错：
# selenium.common.exceptions.StaleElementReferenceException:
# Message: stale element reference: element is not attached to the page document
# 解决方案：通过并行方式，不断循环执行爬虫，通过发送信号方式传递文本信息
