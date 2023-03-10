"""
BOJ 爬虫 USD/JPY  美元对日元 Japaneseyen
爬取的内容为pdf格式
直接向pdf网站发送请求，下载为pdf，将pdf转成一张张图片，解析一张张图片
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import random
import fitz
import re
import time
from PIL import Image
import pytesseract
import socket
import logging
import os
from logging import handlers
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import io


def extract_text_from_pdf(pdf_path):  # 提取文字性的pdf，即pdf中文字可复制
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    if text:
        return text


def send_udp(host, port, message): # 发送udp
    """
    :param host:
    :param port:
    :param message:
    :return:
    爬虫发送至指定端口，一般发到 127.0.0.1
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message.encode('utf-8'), (host, port))


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
                                                                   when='D', encoding="utf-8")
    time_rotating_file_handler.setLevel(logging.DEBUG)
    time_rotating_file_handler.setFormatter(formatter)
    logger.addHandler(time_rotating_file_handler)
    logger.addHandler(stream_handler)
    return logger


logger = log("BOJ")


def pdf2image1(path):
    start = time.time()
    checkIM = r"/Subtype(?= */Image)"
    pdf = fitz.open(path)
    lenXREF = pdf.xref_length()
    count = 1
    if not os.path.exists("img"):
        os.makedirs("img")
    for i in range(1, lenXREF):
        text = pdf.xref_object(i)
        isImage = re.search(checkIM, text)
        if not isImage:
            continue
        pix = fitz.Pixmap(pdf, i)
        if pix.size < 10000:
            continue
        new_name = f"img_{count}.png"

        pix.save(os.path.join('img', new_name))  # pix.save
        count += 1
        # pix = None
    final_text = ""
    for file in os.listdir('img'):
        text = pytesseract.image_to_string(Image.open(r'{}\{}'.format('img', file)), lang="eng")
        final_text += text
    print("pdf转图片+pytesseract识别耗时:", time.time() - start)  # 1.12秒
    return final_text


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
    try:
        driver.get(website)
    except:
        time.sleep(1)
        driver.get(website)
    count = 0
    while True:
        if count <= 10:
            try:
                error_text = driver.find_element(By.XPATH, '//*[@id="contents"]/h1').text
            except:
                error_text = "找到了"
            if (error_text == 'ページが見つかりません | Not Found'):
                logger.info('waiting for data')
                count = count + 1
                time.sleep(random.randint(50, 100) / 1000)
            else:
                url = website
                r = requests.get(url, stream=True)
                with open('BOJ.pdf', 'wb') as fd:
                    for chunk in r.iter_content(4):
                        fd.write(chunk)

                pdf_path = 'BOJ.pdf'
                main_text = pdf2image1(pdf_path)
                if not main_text: # if not picture extract text
                    main_text = extract_text_from_pdf(pdf_path)
                # send_udp("127.0.0.1", 32123, main_text)  # 发送信号
                logger.info('{}'.format(main_text))
                return main_text
        else:
            count = 0
            driver.refresh()
            time.sleep(random.randint(50, 100) / 1000)


if __name__ == '__main__':
    # website = "https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2023/k230118a.pdf"
    website = "https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2023/k230310a.pdf"
    print(website)
    print(main(website))

