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

class Fastfood:

    def __init__(self, version_main=140):
        self.version_main= version_main
        # stop_date_str = pd.read_csv('./天下雜誌/天下雜誌_update.csv')['date'][0]
        # self.stopLineDate = pd.to_datetime(stop_date_str)  
        self.page = 1
        self.articles_list = []
        self.stop_scraping = False # 標記法

    # 拿來關閉阻擋的cookies,因為會使程式無法繼續
    def cookies_block(self,driver):

        try:
            cookies_button = driver.find_element(By.ID,'onetrust-accept-btn-handler')
            cookies_button.click()
            print('✅成功移除cookies阻攔')
        except:
            pass


    def start_driver(self):
        """啟動瀏覽器"""
        print("--------------- 啟動瀏覽器 --------------")
        try:        
            # 能夠通過 Cloudflare
            options = Options()
            # options.add_argument("--incognito")  # 無痕模式
            driver = uc.Chrome(version_main=self.version_main,options=options)
            driver.get(f"https://www.i-fit.com.tw/context/1970.html")
            driver.set_page_load_timeout(15) # 不出來最多等15秒
            wait = WebDriverWait(driver,5)

        except Exception as e:
            print(f'❌瀏覽出問題: {e}')

        

        print("--------------- 登入configuration --------------")


        contentbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.post-content')))
        contents = contentbox.find_elements(By.TAG_NAME,'table')
        for content in contents:
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
            df = pd.DataFrame(data[1:], columns=data[0])

            if os.path.exists('kentucky.json'):
                df_old = pd.read_json('kentucky.json')
                new_df = pd.concat([df_old,df])
                new_df.to_json('kentucky.json',force_ascii=False,indent=4, orient="records")
            else:
                df.to_json('kentucky.json',force_ascii=False,indent=4, orient="records")
            print('-------------------------------')



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
        sys.stdout = Logger("./Kentucky.log")
        sys.stderr = sys.stdout

        try:        
            # 能夠通過 Cloudflare
            options = Options()
            # options.add_argument("--incognito")  # 無痕模式
            driver = uc.Chrome(version_main=self.version_main,options=options)
            driver.get(f"https://www.kfcclub.com.tw/menu?menuId=182")
            driver.set_page_load_timeout(15) # 不出來最多等15秒
            wait = WebDriverWait(driver,5)

        except Exception as e:
            print(f'❌瀏覽出問題: {e}')
        
        infos = []
        contents = driver.find_elements(By.CSS_SELECTOR,'div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.MuiCard-root.styles_root__Ad4_u.css-s18byi')
        for id, content in enumerate(contents):
            title = content.text.split('\n')[0]
            img = content.find_element(By.TAG_NAME,'img').get_attribute('src')
            print(id)
            print(title)
            print('img: ',img)
            print()
            infos.append([title,img])
        

            
        try:
            path = f"./Kentucky_pic"
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
    b = Fastfood()
    # b.crawl_img()

    # with open(r'./info_json/kentucky.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    
    # for d in data:
    #     d["品項"] = d.pop("餐點")
    #     d["熱量"] = d.pop("熱量（大卡）")

    # with open(r'./info_json/kentucky.json', 'w', encoding='utf-8') as f:
    #     json.dump(data,f,indent=4,ensure_ascii=False)
    
    # with open(r'.\info_json\kentucky.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)



    # for d in data:
    #     d['熱量'] == d['熱量'].replace(",","").strip()



    # with open(r'.\info_json\kentucky.json', 'w', encoding='utf-8') as f:
    #     json.dump(data,f,indent=4,ensure_ascii=False)



