
'''
玉林师范学院自动化体温填报
因为疫情原因，学校要求在学校的系统里填报体温
每天都要填一次就很烦，所以就写了这个来让python自己填

识别验证码的是别人训练好的ocr模型
'''

from selenium import webdriver
from time import sleep
from PIL import Image
import tesserocr
import time


def test_a():
    #运行chrome驱动
    d = webdriver.Chrome()
    #窗口最大化
    d.maximize_window()

    url = "http://jx.ylnu.net/xsdj/login.htm1"
    d.get(url)

    d.find_element_by_xpath('//*[@id="UserName"]').send_keys('学号')
    sleep(1)
    d.find_element_by_xpath('//*[@name="pwd"]').send_keys('密码')

    sleep(1)

    d.find_element_by_xpath('//*[@id="CheckCode"]').click() #验证码
    sleep(2)

    #截取验证码
    d.save_screenshot('printscreen.png')
    aa = d.find_element_by_id('chkc') # 定位验证码
    left = aa.location['x'] - 5
    top = aa.location['y'] - 5
    right = aa.location['x'] + aa.size['width'] - 2
    bottom = aa.location['y'] + aa.size['height'] + 5
    im = Image.open('printscreen.png')
    im = im.crop((left, top, right, bottom))
    im.save('nn.png')

    #识别图片
    image = Image.open('nn.png')#打开图片
    image = image.convert('L')#图片转灰度
    # image.save('11.jpg') #保存图片
    img_black_white = image.point(lambda x: 0 if x > 200 else 255)# 转黑白
    a = tesserocr.image_to_text(image)# 识别图片
    print(a)

    sleep(2)
    d.find_element_by_xpath('//*[@id="CheckCode"]').send_keys(a) #验证码

    # d.find_element_by_xpath('//*[@name="Submit"]').click() #登陆

    # 解决弹窗问题
    sleep(3)
    alert = d.switch_to.alert #切换到alert
    print('alert text : ' + alert.text) #打印alert的文本
    alert.accept() #点击alert的【确认】按钮
    sleep(1)

    d.find_element_by_xpath('//*[@name="TW"]').clear()# 清空
    sleep(1)
    d.find_element_by_xpath('//*[@name="TW"]').send_keys('36.5') #填体温
    d.find_element_by_xpath('//*[@name="insert"]').click() #保存

    alert = d.switch_to.alert #切换到alert
    print('alert text2 : ' + alert.text) #打印alert的文本
    alert.accept() #点击alert的【确认】按钮
    sleep(3)

    d.quit()


if __name__=='__main__':
    # 定时填报
    # while True:
    #     t = time.strftime("%H:%M:%S", time.localtime())
    #     if t == '21:28:00':
    #         test_a()
    #         break
    test_a()

