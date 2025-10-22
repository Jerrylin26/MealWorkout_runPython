from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
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

class Mos:

    def __init__(self, version_main=140):
        self.version_main= version_main
        self.page = 1
        self.articles_list = []
        self.stop_scraping = False # 標記法




    def crawl_img(self):

        # 設定 logger
        class Logger:
            def __init__(self, filename="output.log"):
                self.terminal = sys.stdout   # 原本的 console
                self.log = open(filename, "a", encoding="utf-8")

            def write(self, message):
                self.terminal.write(message)   # 照樣印到 console
                self.log.write(message)        # 同時寫進 log
                self.log.flush()               # 立即寫入檔案

            def flush(self):
                pass  # for Python buffer 需求
        
        # 把 stdout 和 stderr 都導向 Logger
        sys.stdout = Logger("./burgerKing.log")
        sys.stderr = sys.stdout

        try:        
            # 能夠通過 Cloudflare
            options = Options()
            # options.add_argument("--incognito")  # 無痕模式
            driver = uc.Chrome(version_main=self.version_main,options=options)
            driver.get(f"https://www.burgerking.com.tw/category/3")
            driver.set_page_load_timeout(15) # 不出來最多等15秒
            wait = WebDriverWait(driver,5)

            time.sleep(2)
            driver.refresh()
            time.sleep(2)

        except Exception as e:
            print(f'❌瀏覽出問題: {e}')
        
        infos = []

        buttons = ['https://www.burgerking.com.tw/category/3','https://www.burgerking.com.tw/category/5','https://www.burgerking.com.tw/category/4']

        for button in buttons:
            
            driver.get(button)
            time.sleep(2)

            contents = driver.find_elements(By.CSS_SELECTOR,'main section')
            print(len(contents))

            for content in contents[:-1]:

                con = content.find_element(By.CSS_SELECTOR,'div.grid.grid-cols-2')
                imgs = con.find_elements(By.TAG_NAME,'img')
                titles = con.find_elements(By.CSS_SELECTOR,'div[class="md:px-0 md:px-10 md:text-xl px-2 text-center text-lg"]')
                print(len(titles))
                for title, img in zip(titles,imgs):
                    print(title.text)
                    print(img.get_attribute('src'))
                    infos.append([title.text,img.get_attribute('src')])
                print()
            

        try:
            path = f"./burgerKing_pic"
            os.makedirs(path, mode=0o777)

        except Exception as e:
            print(f'❌建立資料夾出問題: {e}')

        try:

            for info in infos:
                title = info[0]
                imgs = info[1]

                title = re.sub(r'[\\/:*?"<>|]', '_', title)
                                
                try:
                    
                    thumbnail = requests.get(imgs)
                    with open(f'{path}/{title}.png', 'wb') as f:
                        f.write(thumbnail.content)

                except Exception as e:
                    print(f'❌下載單張圖片出問題: {e}')

                print("✅成功抓到完整圖片")
                
            
        except Exception as e:
            print(f'❌下載圖片出問題: {e}')
                
        
    

if __name__ == "__main__":
    # b = Mos()
    # b.crawl_img()

    # with open(r'./info_json/burger_final.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    
    # for d in data:
    #     d["熱量"] = str(d["熱量"])

    # with open(r'./info_json/burger_final.json', 'w', encoding='utf-8') as f:
    #     json.dump(data,f,indent=4,ensure_ascii=False)

    # with open(r'.\info_json\burger_final.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)



    # for d in data:
    #     d['熱量'] == d['熱量'].replace(",","").strip()



    # with open(r'.\info_json\burger_final.json', 'w', encoding='utf-8') as f:
    #     json.dump(data,f,indent=4,ensure_ascii=False)


