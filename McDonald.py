from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import NewConnectionError
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import datetime
from dateutil.parser import parse
import pandas as pd
from selenium.common.exceptions import TimeoutException
import json
import requests
import os
import sys
import re
import platform


def get_chrome_path():
    if platform.system() == "Windows":
        return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    else:
        # Render Linux 路徑
        print("choose linux")
        return "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"


class McDonald:

    def __init__(self, version_main=140):
        self.version_main= version_main
        self.page = 1
        self.articles_list = []
        self.stop_scraping = False # 標記法



    def start_driver(self):
        print("--------------- 啟動瀏覽器 --------------")
        # try:
        #     options = Options()
        #     options.binary_location = get_chrome_path()
        #     options.add_argument("--headless=new")  # 一定要新版本 headless 模式
        #     options.add_argument("--no-sandbox")
        #     options.add_argument("--disable-dev-shm-usage")
        #     options.add_argument("--disable-gpu")
        #     options.add_argument("--disable-software-rasterizer")
        #     options.add_argument("--disable-extensions")
        #     options.add_argument("--disable-background-networking")
        #     options.add_argument("--disable-default-apps")
        #     options.add_argument("--disable-sync")
        #     options.add_argument("--remote-debugging-port=9222")


        #     driver = webdriver.Chrome( options=options)

        #     driver.set_page_load_timeout(3)
        #     driver.get("https://www.mcdonalds.com/tw/zh-tw/sustainability/good-food/nutrition-calculator.html")
        #     wait = WebDriverWait(driver, 5)

        # except Exception as e:
        #     print(f'❌瀏覽出問題: {e}')
        #     return  # 若 Chrome 啟動失敗，不繼續執行

        # print("--------------- 登入 configuration --------------")

        # data = []
        # contents_count = len(driver.find_elements(By.CSS_SELECTOR, 'li.cmp-product-card'))

        # for i in range(contents_count):
        #     # 每次 loop 都重新抓 contents
        #     contents = driver.find_elements(By.CSS_SELECTOR, 'li.cmp-product-card')
        #     content = contents[i]

        #     # 點進去
        #     button = content.find_element(By.CSS_SELECTOR, 'button')
        #     type = button.text.split('\n')[0]
        #     button.click()
            
        #     print(type)

        #     # 等詳細頁載入完成
        #     ul = wait.until(EC.visibility_of_element_located(
        #         (By.CSS_SELECTOR, 'ul.cmp-product-card-layout__list')
        #     ))

        #     lis = ul.find_elements(By.CSS_SELECTOR, 'li')
        #     for li in lis:
        #         img = li.find_element(By.CSS_SELECTOR,'img').get_attribute('src')
        #         data.append([type] + li.text.split('\n')[:-1] + [img])

        #     # print(data)

        #     # 點返回
        #     back = wait.until(EC.element_to_be_clickable(
        #         (By.CSS_SELECTOR, 'button.cmp-product-card-layout__navigate-button')
        #     ))
        #     back.click()

        #     # 等回到產品卡片頁面
        #     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.cmp-product-card')))
            

        # df = pd.DataFrame(data, columns=['種類','品項','熱量','圖片'])
        # # 修改種類欄位
        # df['種類'] = df['種類'].replace({
        #     '超值全餐': '主餐',
        #     '極選系列': '主餐',
        #     'McCafé®': '冷飲',
        #     '飲料': '冷飲'
        # })

        # for index, row in df.iterrows():
        #     if row['種類'] == "冷飲":
        #         if "熱" in row['品項']:
        #             df.at[index,'種類'] = "熱飲"


        # df.to_json('McDonald.json',force_ascii=False,indent=4, orient="records")

        with open('McDonald.json','r',encoding='utf-8') as f:
            data = f.read()
        data = data.replace('\\/','/')

        # 寫入
        with open('McDonald.json','w',encoding='utf-8') as f:
            f.write(data)


        # 修改column名稱
        with open('McDonald.json','r',encoding='utf-8') as f:
            data = json.load(f)

        for row in data:
            row['種類'] = row['類別']
        
        # 寫入
        with open('McDonald.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
                

if __name__ == "__main__":
    b = McDonald()
    b.start_driver()
    

