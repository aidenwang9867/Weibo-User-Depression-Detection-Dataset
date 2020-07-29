import pandas as pd
import numpy as np
import os
import json
path =r"E:/weiboSpider/weibo"
data_list=[]
for filename in os.listdir(path):
    User_address = path+'/'+filename
    for User_name in os.listdir(User_address):
        dic ={}
        one_user=[]
        dic['User']= filename
        csv_address = User_address+'/'+User_name
        csv_data = pd.read_csv(csv_address)
        csv_text = csv_data['微博正文'].tolist()
        csv_picture=csv_data['原始图片url'].tolist()
        csv_time =csv_data['发布时间'].tolist()
        csv_self =csv_data['是否为原创微博'].tolist()
        csv_thumb =csv_data['点赞数'].tolist()
        csv_comment=csv_data['评论数'].tolist()
        csv_transfer=csv_data['转发数'].tolist()
        self_num=0
        other_num=0
        for i in range(len(csv_text)):
            one_data={}
            one_data['Context']=csv_text[i]
            one_data['time']=csv_time[i]
            one_data['URL'] =csv_picture[i]
            one_data['Thumb-UP']=csv_thumb[i]
            one_data['Comment']=csv_comment[i]
            one_data['Forward']=csv_transfer[i]
            one_user.append(one_data)
            if csv_self[i]:
                self_num+=1
            else:
                other_num+=1
        dic['infor']=one_user
        dic['Original Count:']=self_num
        dic['Reprint Count:']=other_num
    data_list.append(dic)

with open("E:/weiboSpider/User_data.json","w",encoding='utf-8') as f:
    json.dump(data_list,f,ensure_ascii=False)
