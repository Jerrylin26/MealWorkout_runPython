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



    def start_driver(self):
        """啟動瀏覽器"""
        print("--------------- 啟動瀏覽器 --------------")
        try:        
            # 能夠通過 Cloudflare
            options = Options()
            # options.add_argument("--incognito")  # 無痕模式
            driver = uc.Chrome(version_main=self.version_main,options=options)
            driver.get(f"https://rachelee1223.blogspot.com/2009/08/blog-post_25.html")
            driver.set_page_load_timeout(15) # 不出來最多等15秒
            wait = WebDriverWait(driver,5)

        except Exception as e:
            print(f'❌瀏覽出問題: {e}')

        

        print("--------------- 登入configuration --------------")

        data = []
        column = []
        tbody = driver.find_element(By.CSS_SELECTOR, 'div.post-body.entry-content')
        tr = tbody.find_elements(By.CSS_SELECTOR,'tr')
        isTrue = True
        for i in range(len(tr)):
            # 每次 loop 都重新抓 contents
            if ("品項" in tr[i].text):
                print('2')
                if isTrue:
                    isTrue = False
                    print(tr[i].text)
                    column.extend(['類別'] + tr[i].text.split())
                    print(column)

            elif len(tr[i].text.split()) < 2:
                print('3')
                title = tr[i].text
                print(tr[i].text)

            else:
                data.append([title] + tr[i].text.split())
                # print(tr[i].text)
                print('1: ',tr[i].text.split())
        

        df = pd.DataFrame(data, columns=column)
        df.to_json('Mos.json',force_ascii=False,indent=4, orient="records")

        # with open('Mos.json','r',encoding='utf-8') as f:
        #     data = f.read()
        # data = data.replace('\\/','/')
        # with open('Mos.json','w',encoding='utf-8') as f:
        #     f.write(data)


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
        sys.stdout = Logger("./Mos.log")
        sys.stderr = sys.stdout

        try:        
            # 能夠通過 Cloudflare
            options = Options()
            # options.add_argument("--incognito")  # 無痕模式
            driver = uc.Chrome(version_main=self.version_main,options=options)
            driver.get(f"https://www.mos.com.tw/menu/set.aspx")
            driver.set_page_load_timeout(15) # 不出來最多等15秒
            wait = WebDriverWait(driver,5)

        except Exception as e:
            print(f'❌瀏覽出問題: {e}')
        
        infos = []
        count = 1
        buttons = driver.find_elements(By.CSS_SELECTOR,'aside ul li')
        for i in range(len(buttons)):
            if i == 6:
                break

            button = driver.find_elements(By.CSS_SELECTOR,'aside ul li a')[i]
            typeFood = button.text
            time.sleep(1)
            button.click()
            time.sleep(1)
            driver.refresh()
            content_box = driver.find_element(By.CSS_SELECTOR,'ul.productsList')
            contents = content_box.find_elements(By.CSS_SELECTOR,'li')
            print(len(contents))
            
            for id, content in enumerate(contents):
                content = content_box.find_elements(By.CSS_SELECTOR,'li')[id]
                title = content.text
                if title:
                    img = content.find_element(By.TAG_NAME,'img').get_attribute('src')
                    print(count)
                    print(title)
                    href = content.find_element(By.TAG_NAME,'a')
                    href.click()
                    time.sleep(1)
                    try:
                        cal_elem = driver.find_element(By.CSS_SELECTOR, 'tbody tr')
                        cal = cal_elem.text.strip()
                    except:
                        cal = "0"

                    print('img: ',img)
                    print('cal:',cal)
                    print()
                    infos.append({'品項':title,'圖片':img,'熱量':cal,'類別':typeFood})
                    count +=1
                    driver.back()
                    time.sleep(1)
        
            with open(r'.\Mos.json', 'w', encoding='utf-8') as f:
                json.dump(infos,f,indent=4,ensure_ascii=False)

        try:
            path = f"./Mos_pic"
            os.makedirs(path, mode=0o777)

        except Exception as e:
            print(f'❌建立資料夾出問題: {e}')

        try:

            for info in infos:
                title = info['品項']
                imgs = info['圖片']

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


    # with open(r'.\info_json\Mos.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)



    # for d in data:
    #     if d['類別'] == "元氣早餐":
    #         d['類別'] = "早餐"
    #     elif d['類別'] == "副餐":
    #         d['類別'] = "點心"
    #     elif d['類別'] == "MOS Café":
    #         d['類別'] = "冷飲"
    #     elif d['類別'] == "飲品":
    #         d['類別'] = "冷飲"
    #     elif d['類別'] == "甜品":
    #         d['類別'] = "點心"
        

    # with open(r'.\info_json\Mos.json', 'w', encoding='utf-8') as f:
    #     json.dump(data,f,indent=4,ensure_ascii=False)

    # with open(r'.\info_json\Mos.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)



    # for d in data:
    #     d['熱量'] == d['熱量'].replace(",","").strip()



    # with open(r'.\info_json\Mos.json', 'w', encoding='utf-8') as f:
    #     json.dump(data,f,indent=4,ensure_ascii=False)




