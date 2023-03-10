"""
https://www.norges-bank.no/en/  挪威央行利率决议

https://www.norges-bank.no/en/topics/Monetary-policy/Monetary-policy-meetings/2023/january-2023/
"""
from datetime import datetime
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
month_dict = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december"}


def main(website):
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.add_argument("--window-size=1920,1080")  # 界面大小
    options.add_argument("--headless")  # 无界面显示
    options.add_argument("--disable-gpu")  # 禁止gpu
    options.add_argument("--disable-software-rasterizer")  # 无界面
    options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片
    options.add_argument("--disable-extensions")  # 禁用插件加载
    driver = webdriver.Chrome(options=options)
    driver.get(website)
    time.sleep(random.randint(100, 150) / 1000)
    count = 0
    while True:
        if count <= 20:
            try:
                first_catch = driver.find_element(By.XPATH, '//*[@id="article"]/div/div/article/h1').text  # 定位日期是否一致
            except:
                first_catch = "find it"
            if (first_catch == "Page not found (404)"):  # 则为未更新的页面或者不存在的页面
                # print("waiting for data")
                count = count + 1
                time.sleep(random.randint(10, 15) / 1000)
            else:
                try:
                    main_text = driver.find_element(By.CLASS_NAME, 'tab-pane')  # to be changed
                    return main_text.text
                except:
                    pass
        else:
            count = 0
            driver.refresh()
            time.sleep(random.randint(100, 150) / 1000)


if __name__ == '__main__':
    year = 2023
    month = "january"  #to be changed
    website = "https://www.norges-bank.no/en/topics/Monetary-policy/Monetary-policy-meetings/{}/{}-{}/".format(year,
                                                                                                               month,
                                                                                                               year)
    #website = "https://www.norges-bank.no/en/topics/Monetary-policy/Monetary-policy-meetings/2023/january-2023/" test
    print(website)
    print(main(website))
    # start=time.time()
    # print(datetime.now())
    # try:
    #     print(main(website))
    # except:
    #     print(datetime.now())
    #     print(time.time()-start)
