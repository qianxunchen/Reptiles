import requests
import json
from bs4 import BeautifulSoup
import re
from sqlalchemy import create_engine
import pandas as pd

def ha():
    df = messages()
    name = '走饭评论'
    engine = create_engine("mysql+pymysql://root:***@***:3306/***?charset=utf8mb4")
    # engine = create_engine("mysql+pymysql://【此处填用户名】:【此处填密码】@【此处填host】:【此处填port】/【此处填数据库的名称】?charset=utf8")
    df.to_sql(name=name, con=engine, if_exists='replace', index=False)

def messages():
    lists = []
    for i in range(0,10):
        url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=3424883176420210&page=%s&__rnd=1589554452072'%i
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
                    'Accept': '*/*',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive',
            }
        cookies = {'cookies':'微博cookie'}
        data = requests.get(url=url,headers=headers,cookies=cookies)
        # print(data.text.encode('utf-8').decode('unicode_escape'))
        data = json.loads(data.text)
        data1 = data['data']
        data2 = data1['html']
        # print(data2)
        soup = BeautifulSoup(data2, 'lxml', from_encoding='utf-8')
        data = soup.select('div[class="WB_text"]')
        for i in data:
            name = i.select('a')[0].string
            href = i.find_all('a')[0]['href']
            Text = i.text
            s = '：'
            msg = re.split(s, Text)[1]
            # print('微博名：'+name+'  评论：'+msg)
            # print(href)
            lists.append([name, msg, href])
    return pd.DataFrame(lists, columns=['name', 'pinlun', 'href'])



if __name__=="__main__":
    ha()