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

class TKK:

    def __init__(self, version_main=140):
        self.version_main= version_main
        # stop_date_str = pd.read_csv('./天下雜誌/天下雜誌_update.csv')['date'][0]
        # self.stopLineDate = pd.to_datetime(stop_date_str)  
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
            driver.get(f"https://dailydietitian.com.tw/%E9%A0%82%E5%91%B1%E5%91%B1%E8%8F%9C%E5%96%AE%E5%83%B9%E6%A0%BC-%E7%86%B1%E9%87%8F-%E7%87%9F%E9%A4%8A%E6%88%90%E5%88%86/")
            driver.set_page_load_timeout(15) # 不出來最多等15秒
            wait = WebDriverWait(driver,5)

        except Exception as e:
            print(f'❌瀏覽出問題: {e}')

        

        print("--------------- 登入configuration --------------")


        contents = driver.find_elements(By.TAG_NAME,'table')[:3]
        for i, content in enumerate(contents):

            title = []
            ths = content.find_element(By.CSS_SELECTOR,'thead').find_elements(By.CSS_SELECTOR,'th')
            for th in ths:
                title.append(th.text.replace('\n',' '))
            
            print(title)

            if i != 1:

                data = []
                trs = content.find_elements(By.CSS_SELECTOR,'tr')
                for tr in trs:
                    tds = tr.find_elements(By.CSS_SELECTOR,'td')
                    temp = []
                    for td in tds:
                        # print(td.text,end=' ')
                        temp.append(td.text)
                    # print()
                    data.append(temp)
                
                # print(data)
                df = pd.DataFrame(data[1:], columns=title)

                if os.path.exists('TKK.json'):
                    df_old = pd.read_json('TKK.json')
                    new_df = pd.concat([df_old,df])
                    new_df.to_json('TKK.json',force_ascii=False,indent=4, orient="records")
                else:
                    df.to_json('TKK.json',force_ascii=False,indent=4, orient="records")
                print('--   -----------------------------')

            else:
                data = []
                trs = content.find_elements(By.CSS_SELECTOR,'tr')
                for tr in trs:
                    tds = tr.find_elements(By.CSS_SELECTOR,'td')
                    temp = []
                    for td in tds:
                        # print(td.text,end=' ')
                        temp.append(td.text)
                    # print()
                    data.append(temp)
                
                print(data)
                df = pd.DataFrame(data[1:], columns=title)
                df.to_json('TKK_1.json',force_ascii=False,indent=4, orient="records")

    
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
        sys.stdout = Logger("./TKK.log")
        sys.stderr = sys.stdout

        try:        
            # 能夠通過 Cloudflare
            options = Options()
            # options.add_argument("--incognito")  # 無痕模式
            driver = uc.Chrome(version_main=self.version_main,options=options)
            driver.get(f"https://www.tkkinc.com.tw/sideDish.html")
            driver.set_page_load_timeout(15) # 不出來最多等15秒
            wait = WebDriverWait(driver,5)

        except Exception as e:
            print(f'❌瀏覽出問題: {e}')
        
        # 點擊刷新js
        more_content = driver.find_element(By.CSS_SELECTOR,'a.more--content')

        while "display: none" not in more_content.get_attribute('outerHTML'):
            more_content.click()
            time.sleep(1)

        type_button = driver.find_elements(By.CSS_SELECTOR,'a.buttons--content')
        
        infos = []

        for i in range(len(type_button[1:])):
            if i == 2:
                break
            type_button = driver.find_elements(By.CSS_SELECTOR,'a.buttons--content')[i+1]
            time.sleep(1)
            contents = driver.find_elements(By.CSS_SELECTOR,'div.row--combo div.col')

            for content in contents:
 
                title = content.text.split('\n')[0]
                img = content.find_element(By.CSS_SELECTOR,'img').get_attribute('src')
                print('title: ',title)
                print('img: ',img)
                print()
                infos.append([title,img])

            type_button.click()
            time.sleep(1)

        
        try:
            path = f"./TKK_pic"
            os.makedirs(path, mode=0o777)

        except Exception as e:
            print(f'❌建立資料夾出問題: {e}')

        try:

            

            for info in infos:
                title = info[0]
                imgs = info[1]
                                
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
    b = TKK()
    # b.crawl_img()
    # b.start_driver()

    # with open(r'./info_json/TKK/TKK.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    
    # for d in data:
    #     d["熱量"] = d.pop("熱量 kcal")

    # with open(r'./info_json/TKK/TKK.json', 'w', encoding='utf-8') as f:
    #     json.dump(data,f,indent=4,ensure_ascii=False)

    with open(r'.\info_json\TKK.json', 'r', encoding='utf-8') as f:
        data = json.load(f)



    for d in data:
        d['熱量'] = d['熱量'].replace(",","").replace("–","0").strip()



    with open(r'.\info_json\TKK.json', 'w', encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)



