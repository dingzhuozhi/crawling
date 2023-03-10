import time
import random
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


def Send(model_ip, model_port, monitor_ip, monitor_port, ID_list):  # ip地址
    def send_udp(host, port, message):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(message.encode('utf-8'), (host, port))

    # 启动时向监控端口发送字符串
    monitor_host = monitor_ip
    monitor_port = monitor_port
    # send_udp(monitor_host, monitor_port, "crawler")

    # 向模型端口循环发送信息
    host = model_ip
    port = model_port
    mobileEmulation = {"deviceName": "iPad"}
    # 实例化谷歌浏览器加载项
    options = webdriver.ChromeOptions()  # 谷歌浏览器
    options.page_load_strategy = 'eager'
    options.add_argument("--window-size=1920,1080")  # 界面大小
    options.add_argument("--headless")  # 无界面显示
    options.add_argument("--disable-gpu")  # 禁止gpu
    options.add_argument("--disable-software-rasterizer")  # 无界面
    options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片
    options.add_argument("--disable-extensions")  # 禁用插件加载
    options.add_experimental_option("mobileEmulation", mobileEmulation)  # 添加模拟参数
    driver = webdriver.Chrome(options=options)  # 谷歌浏览器
    driver.get("https://cn.investing.com/economic-calendar/")  # 实时更新的网站

    count = 0
    while count < 4000:  # 跑2000个
        msg_list = []
        msg = ""
        for ID in ID_list:
            if len(driver.find_element(By.ID, ID).text) == 1:
                print("{}数据尚未更新".format(datetime.now()))
                time.sleep(random.randint(5, 10) / 1000)
            else:
                print("捕捉成功,当前时间为:", datetime.now())
                msg_list.append(driver.find_element(By.ID, ID).text.replace("%", ""))
        # 判断结果是否完全，防止部分数据尚未更新或者当前进程中未被抓取
        if len(msg_list) == len(ID_list):
            for item in msg_list:
                msg += str(item) + ","
            print("抓取的三条记录为:", msg)
            message = msg
            # send_udp(host, port, message)
        else:
            continue
        count += 1
        print("每组数据的抓取时间", datetime.now())
        if count % 2000 == 0:  # 抓取2000次后，进行页面刷新,以防反爬
            driver.refresh()  # 进行页面刷新
            time.sleep(random.randint(5,10)/1000)


# cpi需要爬取 12个值
def main():  # 需要修改以下5个参数
    model_ip = "192.168.7.111"  # 模型ip
    model_port = 30000
    monitor_ip = "192.168.7.66"  # 监视ip
    monitor_port = 30002
    ID_list = ['eventActual_460941', 'eventForecast_460941', 'eventPrevious_460941',
               'eventActual_460943', 'eventForecast_460943', 'eventPrevious_460943',
               'eventActual_460942', 'eventForecast_460942', 'eventPrevious_460942',
               'eventActual_460944', 'eventForecast_460944', 'eventPrevious_460944']  # cpi四个特征的今值，预测值，前值

    Send(model_ip, model_port, monitor_ip, monitor_port, ID_list)


if __name__ == "__main__":
    main()
