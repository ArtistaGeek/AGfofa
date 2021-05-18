#! /usr/bin/env python3 
# -*- coding:utf-8 -*- 
# ====#====#====#====
# Author    : 声东
# Datetime  : 16/5/21 10:23 上午
# Product   : PyCharm
# Project   : AGfofa
# File      : AGfofa.py
# explain   : 一个简单的fofa采集器，参考bgbingfofa，自己练手，改进了一下
# ====#====#====#====
import base64
import configparser #读取config文件
import json
import os
import requests


def banner():
    print('''
\033[1;32m       db          ,ad8888ba,     ad88                ad88    \033[0m
\033[1;32m      d88b        d8"'    `"8b   d8"                 d8"      \033[0m
\033[1;32m     d8'`8b      d8'             88                  88        \033[0m
\033[1;34m    d8'  `8b     88            MM88MMM  ,adPPYba,  MM88MMM ,adPPYYba, \033[0m
\033[1;34m   d8YaaaaY8b    88      88888   88    a8"     "8a   88    ""     `Y8 \033[0m
\033[1;34m  d8""""""""8b   Y8,        88   88    8b       d8   88    ,adPPPPP88 \033[0m
\033[1;32m d8'        `8b   Y8a.    .a88   88    "8a,   ,a8"   88    88,    ,88 \033[0m
\033[1;32md8'          `8b   `"Y88888P"    88     `"YbbdP"'    88    `"8bbdP"Y8 \033[0m

\033[1;32m*===============================================* \033[0m
\033[1;32m|    Author:声东                                 | \033[0m
\033[1;32m|    Version:1.0                                | \033[0m
\033[1;32m|    Time:2021/5/16                             | \033[0m
\033[1;32m|    Note:初次使用请将email和key写入config文件中     | \033[0m
\033[1;32m*===============================================* \033[0m
    ''')

#获取AGfofa.config文件中的email和key
def get_key():
    # 获取config文件路径
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "AGfofa.config")
    # 创建管理对象
    conf = configparser.ConfigParser()
    # 读config文件
    conf.read(cfgpath, encoding="utf-8")
    # 取出文件中config这个部分里的email和key对应的内容
    email = conf.get('config', 'email')
    key = conf.get('config', 'key')
    return(email,key)

def get_ip():
    sentence = input("\033[1;32mfofa语句 >>> \033[0m")   #输入fofa语句
    amount = input("\033[1;32m采集数量(<=10000) >>> \033[0m")  #输入要采集的ip条数
    resultsname = sentence + '.txt'
    sentence = base64.b64encode(sentence.encode('utf-8')).decode("utf-8")   #对fofa语句进行base64加密
    url = 'https://fofa.so/api/v1/search/all?email=' + email + '&key=' + key + '&qbase64=' + sentence+'&size='+ amount  #调用fofaapi
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; IntelMacOS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 / 537.36"
    }
    response = requests.get(url, headers=header)    #得到api的返回
    #print(response.text)
    if 'errmsg' not in response.text:
        a = json.loads(response.text)  #将json数据转换成python字典
        print('\033[1;32m成功采集到以下ip并保存至\033[0m'+ resultsname)
        for i in a['results']:
            s = i[0]
            print(s)
            f = open( resultsname,'a')
            f.write(s + "\n")
    elif '401' in response.text:
        print('\033[1;32merror：email或key不正确\033[0m')
    elif 'query statement error' in response.text:
        print('\033[1;32merror：fofa语句不正确\033[0m')
    else:
        print('\033[1;32merror：未知错误\033[0m')


if __name__ == '__main__':
    banner()
    (email,key)= get_key()
    while(1):
        get_ip()


