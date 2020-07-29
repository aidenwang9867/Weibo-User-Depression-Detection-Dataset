import pandas as pd 
import json 

def  judge():
    with open(r'C:\Users\12068\Desktop\black_users\new_black_tag.json','r') as f:
        json_data = f.read()
    list1=json_data.split('}')
    user_list=[]
    del(list1[-1])
    for i in range(len(list1)):
        list1[i]+="}"
        list1[i]=list1[i].replace('\n', '').replace('\r', '')
        if(list(eval(list1[i]).values())[0] =='1'):
            a=list(eval(list1[i]).keys())[0]
        else:
            continue
        user_list.append(a)
    return user_list

black_users = judge()
json_data2=[]
json_data3=[]
user_info=[]

with open(r'C:\Users\12068\Desktop\black_users\new_black_data1.json','r',encoding='utf-8')as f1:
    for line in f1:
        a = json.loads(line)
        json_data2.append(a)

json_data=json_data2

with open(r'C:\Users\12068\Desktop\black_users\Users.json','r',encoding='utf_8') as f3:
    user_info = json.load(f3)

total=[]
for i in range(len(black_users)):
    one_user={}
    all_info=[]
    self_num=0
    transfer_num=0
    for j in range(len(user_info)):
        if(user_info[j]['_id'] == black_users[i]):
            try:
                one_user['User'] = user_info[j]['nick_name']
            except:
                print(user_info[j]['_id'])
                one_user['User'] ='未获取'
            one_user['ID'] = user_info[j]['_id']
            try:
                one_user['Sex'] = user_info[j]['gender']
            except:
                print(user_info[j]['_id'])
                one_user['Sex'] ='未获取'
            try:
                one_user['Birth'] = user_info[j]['birthday']
            except:
                one_user['Birth'] = '无'
            one_user['Number of fans'] =user_info[j]['fans_num']
            one_user['Micro-blog number'] =user_info[j]['tweets_num']
            one_user['Concern number'] =user_info[j]['follows_num']
            try:
                one_user['brief introduction'] =user_info[j]['brief_introduction']
            except:
                one_user['brief introduction'] = '无'
            one_user['label'] ='1'
            break
    
    #if('User' not in list(one_user.keys())):
    #    continue
    for k in range(len(json_data)):
        one_info={}
        if(json_data[k]['user_id']==black_users[i]):
            one_info['Context']=json_data[k]['content'] 
            one_info['time']=json_data[k]['created_at'] 
            try:
                one_info['URL']=json_data[k]['image_url']
            except:
                one_info['URL']='无'
            one_info['Thumb-UP']=json_data[k]['like_num'] 
            one_info['Comment']=json_data[k]['comment_num'] 
            one_info['Forward']=json_data[k]['repost_num']
            if('转发理由:' in json_data[k]['content']): 
                one_info['Self']='False'
                transfer_num+=1
            else:
                one_info['Self']='True'
                self_num+=1
            all_info.append(one_info)
        else:
            continue
    one_user['infor']=all_info
    one_user['Original Count:']=self_num
    one_user['Reprint Count:']=transfer_num
    total.append(one_user)

with open(r'C:\Users\12068\Desktop\black_users\5.20_black.json','w',encoding='utf-8') as f2:
    json.dump(total,f2,ensure_ascii=False)




    
