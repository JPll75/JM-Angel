import requests
import urllib.request
import webbrowser
import json
from selenium import webdriver
from PIL import Image
import time

global url_delete


def upload(path):
    global url_delete
    headers = {'Authorization': 'Your_Token'}
    files = {'smfile': open(path, 'rb')}
    url = 'https://sm.ms/api/v2/upload'
    res = requests.post(url, files=files, headers=headers).json()
    data = res.get('data')
    url_get = data.get('url')
    url_delete = data.get('delete')
    print("[Info] File image URL is: " + url_get)
    return url_get


"""
从本地上传图片至图床，调用方式：
    传入的参数path为文件在本地的路径，调用sm.ms图床的api，将图片上传至sm.ms图床。
    headers终的Authoriazation字段中应填写自己的API Token，获取方法：
        进入https://sm.ms/，登陆后，在User选项的下拉条选择Dashboard
        点击进入，在左侧导航栏中找到API Token选项。
        复制Secret Token，如果没有，则先点击Generate Secret Token生成令牌后再复制
    
    **注意**
    这个函数使用的是sm.ms图床，不同的图床回传的数据格式可能不一样
    如使用其它图床请根据自身情况调整
"""


def delet_img():
    global url_delete
    url = url_delete
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    driver.quit()
    return


"""
删除图床中刚上传的文件，调用方式：
    在调用upload函数之后，会给delet_img传送删除图床图片的api，
    此时调用delet_img即可删除刚刚上传的图片。
    通过此方法可以实现同一张图片的重复上传并发送，避免图床提示文件已存在。
    
    ps：
    使用过程中selenium报错handshake error可以忽略（
    因为我暂时没想到更好的方法访问url（捂脸）
"""

if __name__ == "__main__":
    upload('../imgs/img_test.jpg')
    time.sleep(4)
    delet_img()
