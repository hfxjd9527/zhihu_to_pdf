# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pdfkit
import os
import PyPDF2


class zhihu_infos:
    # 定义一个zhihu类
    def __init__(self):
        # 对象初始化
        url = 'https://www.zhihu.com/signup'
        self.url = url

        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 30)  # 超时时长为30s

        self.pdf_path = "./pdf_file/"
        if not os.path.exists(self.pdf_path):
            os.makedirs(self.pdf_path)

        self.html_path = "./html_file/"
        if not os.path.exists(self.html_path):
            os.makedirs(self.html_path)

    def login(self):
        # 登录知乎
        # 打开网页
        self.browser.get(self.url)
        self.browser.maximize_window()
        # 等待 登录选项 出现，并点击
        password_login = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.SignContainer-switch > span:nth-child(1)')))
        password_login.click()
        time.sleep(3)
        # 等待 账号 出现
        zhihu_user = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.SignFlow-accountInput > input:nth-child(1)')))
        zhihu_user.send_keys(zhihu_username)

        # 等待 密码 出现
        zhihu_pwd = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 '.SignFlow-password > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)')))
        zhihu_pwd.send_keys(zhihu_password)

        # 等待 登录按钮 出现
        submit = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'button.Button:nth-child(5)')))
        submit.click()
        time.sleep(10)

    def get_pagesource(self, url):
        self.browser.get(url=url)
        self.browser.maximize_window()
        time.sleep(5)

        # 执行点击动作
        for j in range(1, 21):
            content_click = '#Profile-answers > div:nth-child(2) > div:nth-child(' + str(
                j) + ') > div > div.RichContent.is-collapsed > div.RichContent-inner'
            try:
                complete_content = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, content_click)))
                complete_content.click()
                time.sleep(1)
            except BaseException:
                pass
        pagedata = self.browser.page_source
        return pagedata

    def save_to_html(self, base_file_name, pagedata):
        filename = base_file_name + ".html"
        with open(self.html_path + filename, "wb") as f:
            f.write(pagedata.encode("utf-8", "ignore"))
            f.close()
        return filename

    def html_to_pdf(self, base_file_name, htmlname):
        pdfname = base_file_name + ".pdf"
        htmlfile = open(self.html_path + htmlname, 'r', encoding='utf-8')
        confg = pdfkit.configuration(
            wkhtmltopdf=r'D:\htmlpdf\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_url(htmlfile, self.pdf_path + pdfname, configuration=confg)

    def Many_to_one(self):
        # 找出所有的pdf文件,并将文件名保存至列表。
        filelist = []
        for filename in os.listdir('./pdf_file'):
            if filename.endswith('.pdf'):
                filelist.append(filename)

        # 创建一个新的pdf
        newPdfFile = PyPDF2.PdfFileWriter()

        # 循环打开每一个pdf文件，将内容添加至新的pdf
        for filename in filelist:
            pdfFile = open('./pdf_file/' + filename, 'rb')
            pdfObj = PyPDF2.PdfFileReader(pdfFile)
            # 获取页数
            pageNum = pdfObj.numPages

            for num in range(1, pageNum):
                pageContent = pdfObj.getPage(num)
                newPdfFile.addPage(pageContent)

        newFile = open(self.pdf_path + '恶喵的奶爸.pdf', 'wb')
        newPdfFile.write(newFile)
        newFile.close()


if __name__ == "__main__":
    zhihu_username = "你的账号"
    zhihu_password = "你的密码"
    z = zhihu_infos()
    z.login()
    # 这里作为练习，只爬3页
    for i in range(1, 4):
        url = 'https://www.zhihu.com/people/e-miao-de-nai-ba/answers?page=' + \
            str(i)
        pagedata = z.get_pagesource(url)
        base_file_name = "zhihu{}".format(i)
        htmlname = z.save_to_html(base_file_name, pagedata)
        z.html_to_pdf(base_file_name, htmlname)
    time.sleep(5)
    z.Many_to_one()
