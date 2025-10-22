from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers import TesseractBlobParser
import json
import pandas as pd
from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader
from bs4 import BeautifulSoup


# 用html
"""
with open('D:\code\Langchain_大型ReAct\Langchain_ReAct書\page_1.html', 'r', encoding='utf-8') as f:
    data = f.read()

data = data.split('''
<br></span></div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:427px; top:2831px; width:40px; height:8px;"><span style="font-family: DFHei-W3-WIN-BF; font-size:8px">漢堡王提供
''')

print('len(data): ',len(data))

dat = data[1]

dat = dat.split('''<br></span></div><span style="position:absolute; border: black 1px solid; left:176px; top:2863px; width:399px; height:11px;"></span>''')
dat = dat[0]


data_0 = BeautifulSoup(dat,'html.parser')
# print(data_0.text)

dd = str(data_0.text).split('here')[0].split('\n')
# print(dd)

data_list = []
a = ""
for idx, d in enumerate(dd):
    if (idx+1)%4 == 0 and idx!=0:
        a += d + " "
        a = a.split()
        data_list.append(a)
        a = ""
        print(d)
    else:
        a += d + " "
        print(d,end=' ')

# print(data_list)

dd = str(data_0.text).replace('漢堡王提供','').replace('第三方檢驗','').split('here')[1].strip().split('\n')
for idx, d in enumerate(dd):
    if (idx+1)%5 == 0 and idx!=0:
        a += d + " "
        a = a.split()
        data_list[idx//5].extend(a)
        a = ""
        print(d)
    else:
        a += d + " "
        print(d,end=' ')
print(data_list)
"""



loader = PyPDFLoader(
    r"C:\Users\jerry\OneDrive\Desktop\漢堡王.pdf",
    #extract_images=True,
    images_inner_format='html-img',
    images_parser=TesseractBlobParser(),
)
data = []

docs = list(loader.lazy_load())

istrue = False

for x in docs[5:]:
    infos = str(x).split('4.9 11.4 242.7 漢堡王提供')[0].replace('漢堡王提供','').split('\n')
    
    for info in infos:
        if info.startswith('4'):
            a = info.split()

            if len(a) == 11:
                del a[4:6]

            elif len(a) == 10:
                del a[4]

            data.append(a)
            # print(len(a),a)

    


    infos = str(x).split('4 23 黃金炸雞(排) 59 黃金炸雞(排) 175.0 25.0 31.2 10.0 420.0 漢堡王提供')[1].split('5179.4')[0].replace('漢堡王提供','').split('\n')
    print()
    isfirst = True
    temp = []
    for info in infos:
        if info.startswith('4') and len(info) > 1:
            if isfirst:
                isfirst = False
                continue
                
            else:
                temp.append(info.split())
                # print(info)

    
 
    
    last = [['4.9', '11.4', '242.7'],['70.5', '356.2'],['379.4'],['13','27', '280'],['3.2', '8', '86.5', '428.7'],['9.2', '95.2', '474.4'],['9.4','104.7','517']]

    for i,t in enumerate(temp):
        t.extend(last[i])

    # print(temp)

    data.extend(temp)



    # print(infos)

    new = [['4','19','BK脆雞沙拉','99','190.3','13.4','13.1','20.1','248.3'],['4','20','BK火烤牛肉沙拉','99','190.4','12.8','11.7','8.7','185.0']]

    data.extend(new)

    data.sort(key=lambda x: int(x[1]))

    for d in data:
        print(d)

    break

# column = ['類別', '項次', '品項名稱', '售價', '每價(公克)','蛋白質(公克)','脂肪(公克)','醣類(公克)','熱量(大卡)']

# df = pd.DataFrame(data,columns=column)
# df.to_json(r'D:\code\Langchain_大型ReAct\Langchain_ReAct書\Project\burger_700.json',indent=4,orient='records',force_ascii=False)

