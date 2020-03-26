# -*- coding: utf-8 -*-

'''
爬取新浪财经的股票交易明细存入mysql中
股票代码是手填了几个，正在研究怎么从文件中读取股票代码
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine


def syb():
    global sybmol
    sybmols = ['sh603093','sh600519','sz000725']
    for sybmol in sybmols:
        df = rich()
        # /*--------------------------存入数据库--------------------*/
        engine = create_engine("mysql+pymysql://root:xxx@localhost:3306/study?charset=utf8")
        # engine = create_engine("mysql+pymysql://【此处填用户名】:【此处填密码】@【此处填host】:【此处填port】/【此处填数据库的名称】?charset=utf8")
        df.to_sql(name=sybmol, con=engine, if_exists='replace', index=False)# if_exists='replace'自动建表
        # /*--------------------------存入csv文件-------------------*/
        # df.to_csv(sybmol+'.csv', encoding='utf_8_sig', index=False)

# /*----------------------------爬取信息--------------------------*/
def rich():
    lists = []
    for i in range(10):
        # IP = {'http': '121.237.148.115:3000'}# 使用ip代理
        url = "https://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=%s&date=2020-03-04&page=%s"
        URL = url % (sybmol, i)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        # data = requests.get(url=URL,headers=headers)
        IP = {'http': '125.123.143.60:9999'}
        data = requests.get(url=URL,headers=headers, proxies=IP)
        data.encoding = data.apparent_encoding #解决乱码问题
        data = data.text
        soup = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
        data = soup.select('table[id="datatbl"]')[0]
        data1 = data.find_all("tr")

        for i in data1[1:]:
            time     =  i.select('th')[0].text
            price    =  i.select('td')[0].text
            pchange  =  i.select('td')[1].text
            chenjiao =  i.select('td')[3].text
            xingzhi  =  i.select('th')[1].text
            lists.append([time, price, pchange, chenjiao, xingzhi])
    return pd.DataFrame(lists, columns=['成交时间', '单价', '幅度', '成交量', '性质'])


if __name__ == '__main__':
    syb()






