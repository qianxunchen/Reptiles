
'''
因为学习爬虫爬取网站信息容易被封ip
所以就爬取了西刺ip中的IP来做代理
因为只是当作练习，所以并没有存入数据库中
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd




# 爬取西刺ip
def get_ip(url,D):
    url1 = "https://www.baidu.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    # 通过requests的get方法访问目标网站，获得响应对象
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    URL = url
    D = D
    IP = {'http': '222.95.144.89:3000'}#使用ip代理
    data = requests.get(url=URL, headers=headers, proxies=IP)
    # data = requests.get(url=URL, headers=headers)#不使用代理
    data = data.text
    soup = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
    data = soup.select('tr[class="odd"]')
    for i in data:
        ip = i.select('td')[1].text
        port = i.select('td')[2].text
        portotool = i.select('td')[5].text
        #验证IP可用性
        try:
            porxy = {'http': ip + ":" + port}#组合ip
            res = requests.get(url=url1, headers=Headers, proxies=porxy, timeout=2.0)#请求url
            # 验证响应码
            if res.status_code == 200:
                print("可用:" + '类型:' + portotool)
                print("ip地址：" + ip + ":" + port)
                if portotool == 'HTTP':
                    D.append(ip + ':' + port)
            else:
                print("no!")
        except:
            print("不可用！")

def for_ip():
    D = []
    for i in range(2,10):
        url = "https://www.xicidaili.com/nn/%s" % i
        get_ip(url,D)

    Data = pd.DataFrame(data=D)
    Data.to_csv('./西刺ip.csv')
    print(D)
    print(len(D))
    print(type(D))


if __name__=='__main__':
    for_ip()




