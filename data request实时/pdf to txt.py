import sys
import importlib
importlib.reload(sys)
import os
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import pandas as pd
def file_name(path):
    dirs = os.listdir(path)
    return dirs
pdf_path_list=file_name(r"D:\pachong\BOJ历史文本")
print(pdf_path_list[:-1])
date_list= file_name(r"/BOJ历史文本")[:-1]
date_list=[i[:9] for i in date_list]
text_list=[]
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
    text = fake_file_handle.getvalue()
# close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        return text



if __name__ == '__main__':
    for pdf_path in pdf_path_list[:-1]:
        try:
            text_list.append(extract_text_from_pdf(pdf_path))
        except:
            text_list.append("not pdf")
    print(text_list)
    print(len(text_list))
    count =0
    for i in text_list:
        if i=="not pdf":
            count+=1
    print(count)
    boj_data=pd.DataFrame({"date":date_list,"text":text_list})
    boj_data.to_csv(r"D:\pachong\boj_data.csv",index=False)