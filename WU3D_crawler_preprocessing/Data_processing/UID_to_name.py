import sys
from urllib.parse import quote
import requests
from lxml import etree
import time
import pandas as pd
import numpy as np

def get_uid(name,new_header):
    url = "https://weibo.cn/find/user"
    username = quote(name)
    data = "keyword="+username+"&suser=2"
    response = requests.post(url=url, data=data, headers=new_header)
    selector = etree.HTML(response.content)
    target = selector.xpath("/html/body/table[1]/tr/td[2]/div/form")[0]
    temp = target.attrib['action']
    uid = temp[temp.find('=')+1: temp.find('&')]
    return(uid)

raw_header ="""
Host: weibo.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: https://weibo.cn/find/user
Content-Type: application/x-www-form-urlencoded
Content-Length: 34
Origin: https://weibo.cn
Connection: keep-alive
Cookie: _T_WM=10744839547; SUB=_2A25zjeUZDeRhGeBN7VQX9yrFwjWIHXVRcYtRrDV6PUJbktANLWrdkW1NRFQdO2Azish6ijqKnwDmUlkIJceH4xvO; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhAk76BHi0zoSTaqMMMbivP5JpX5KzhUgL.Foq0SoqcS0B41K.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMce0qcSoMX1K.4; SUHB=0YhRH_SwgpVRC2; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231583
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
TE: Trailers
"""
new_header = {}
fields = raw_header.split("\n")
# print(fields)
for field in fields:
    k_v = field.split(': ')
    if len(k_v) == 2:
        key = k_v[0]
        value = k_v[1]
        new_header[key] = value
data1 =pd.read_csv(r"C:\Users\12068\Desktop\1\4\weibo\抑郁+药\抑郁+药.csv",usecols=[0,1,2])
'''
data2 =pd.read_csv(r"E:/weiboSpider/Project/UserID2.csv",usecols=[0,1,2])
data3 =pd.read_csv(r"E:/weiboSpider/Project/UserID3.csv",usecols=[0,1,2])
'''
User_ID1 =data1['用户id']
User_name1 =data1['用户昵称']
'''
User_ID2 =data2['用户id']
User_ID2 =User_ID2.tolist()
User_name2 =data2['用户昵称']
User_name2=User_name2.tolist()

User_ID3 =data3['用户id']
User_ID3 =User_ID3.tolist()
User_name3 =data3['用户昵称']
User_name3=User_name3.tolist()
'''
for i in range(len(User_ID1)):
    if(User_ID1.loc[i] == '用户id'):
        continue
    elif (User_ID1.loc[i].isdigit()):
        continue 
    else:
        try:
            User_ID1.loc[i]=get_uid(User_name1.loc[i],new_header)
        except:
            continue
        else:
            time.sleep(1)
            print(User_name1.loc[i])
data1.to_csv(r"C:\Users\12068\Desktop\1\4\weibo\抑郁+药\抑郁+药.csv",index=0,encoding='utf_8_sig')