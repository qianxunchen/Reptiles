'''
爬取链家租房信息
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd



def text():
    ips = ["115.219.108.246:8010", "117.88.5.135:3000", "114.223.208.165:8118"]
    Lists = []
    for page in range(2,100):
        url = "https://sz.lianjia.com/zufang/pg%s/#contentList" % page
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        ip = ips[-1]
        IP = {'http': ip}
        data = requests.get(url=url, headers=headers, proxies=IP)
        # data = requests.get(url=url,headers=headers)
        data = data.text
        if data.status_code == 200:
            soup = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
            data = soup.select('div[class="content__list"]')[0]
            data1 = data.select('div[class="content__list--item"]')
            for i in data1:
                data = i.select('div[class="content__list--item--main"]')[0]
                des = data.select('p[class="content__list--item--des"]')[0]
                diqu = des.find_all("a")[0].text
                jiedao = des.find_all("a")[1].text
                xiaoqu = des.find_all("a")[2].text
                mianji = des.find_all("i")[0].next_sibling.strip()
                price = data.select('span[class="content__list--item-price"]')[0]
                price = price.text
                Lists.append([diqu, jiedao, xiaoqu, mianji, price])
                # print(diqu,jiedao,xiaoqu,mianji,price)
        else:
            ips.pop()
            print("在第%s次IP被封" % i)
            # print(s)
            continue
    return pd.DataFrame(Lists, columns=['地区', '街道', '小区', '面积', '租金'])


print(text())

df = text()
df.to_csv('链家.csv', encoding='utf_8_sig', index=False)