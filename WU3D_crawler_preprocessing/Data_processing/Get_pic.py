import queue
import json 
from urllib import request 
import os
import pandas as pd 
import socket
import threading
socket.setdefaulttimeout(30)


def callback(blocknum, blocksize, totalsize):
    '''
    :param blocknum: 已下载数据块
    :param blocksize: 数据块大小
    :param totalsize: 远程文件大小
    :return:
    '''
    percent = 100.0*blocknum*blocksize/totalsize
    if(percent>100):
        percent = 100
    print('%.2f%%' % percent)

def get_pic(url_list):
    path = r'C:/Users/12068/Desktop/pic'
    for i in range(len(url_list)):
        try:
            path_file = path+r'/'+str(url_list[i]['ID'])
        except:
            continue 
        if not os.path.exists(path_file):
            os.mkdir(path_file)
        else:
            continue
        for j in range(len(url_list[i]['infor'])):
            if(url_list[i]['infor'][j]['URL']=='无' or url_list[i]['infor'][j]['Self']=='False' ):
                continue
            else:
                for mount in range(len(url_list[i]['infor'][j]['URL'])):
                    url=url_list[i]['infor'][j]['URL'][mount]
                    url = url.replace('wap180','bmiddle')
                    url = url.replace('large','bmiddle')
                    print(url)
                    o = url.split('/')[-1]
                    name = path_file+r'/'+str(o)
                    try:
                        request.urlretrieve(url,name,callback)
                    except:
                        print('error')


def main():
    list1=list2=list3=list4=list5=[]
    with open(r'C:\Users\12068\Desktop\打标签_王一丁\spider_wyd_vps_02 - 副本\User_data_4.0.json','r',encoding='utf_8') as f:
        json_data = json.load(f)
    along=len(json_data)
    for i in range(along):
        if 0<=i<along/5:
            list1.append(json_data[i])
        elif along/5<=i<(along*2)/5:
            list2.append(json_data[i])
        elif (along*2)/5<=i<(along*3)/5:
            list3.append(json_data[i])
        elif (along*3)/5<=i<(along*4)/5:
            list4.append(json_data[i])
        else:
            list5.append(json_data[i])
    t1 = threading.Thread(target=get_pic, args=(list1, ))
    t2 = threading.Thread(target=get_pic, args=(list2, ))
    t3 = threading.Thread(target=get_pic, args=(list3, ))
    t4 = threading.Thread(target=get_pic, args=(list4, ))
    t5 = threading.Thread(target=get_pic, args=(list5, ))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    print('Exit!')
if __name__=='__main__':
    main()