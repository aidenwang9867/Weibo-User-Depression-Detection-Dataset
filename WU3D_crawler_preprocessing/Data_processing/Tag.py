# coding=utf-8
import pandas as pd 
import json 
import sys
import harvesttext as ht
import re
def weibo_filter(content, repstr=''):
    try:
        co = re.compile('[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile('[\uD800-\uDBFF][\uDC00-\uDFFF]')
    content = co.sub(repstr, content)

    ht0 = ht.HarvestText()
    content = ht0.clean_text(content, 
                             remove_url=True, remove_tags=True, 
                                weibo_at=True, remove_puncts=True)
    return content

def  judge():
    with open(r'C:\Users\12068\Desktop\black_users\new_black_tag.json','r') as f:
        json_data = f.read()
    list1=json_data.split('}')
    user_list=[]
    del(list1[-1])
    for i in range(len(list1)):
        list1[i]+="}"
        list1[i]=list1[i].replace('\n', '').replace('\r', '')
        a=list(eval(list1[i]).keys())[0]
        user_list.append(a)
    return user_list

index=[]
json_data=[]
with open(r'C:\Users\12068\Desktop\black_users\new_black_data1.json','r',encoding='utf_8_sig') as f:
    #json_data = json.load(f)
    for line in f:
        json_data.append(eval(line))
user_list=[]
for i in range(len(json_data)):
    user_list.append(json_data[i]['user_id'])
user_list=list(set(user_list))
print(len(user_list))
old_user = judge()
for i in range(len(old_user)):
    for j in range(len(user_list)):
        if(user_list[j]==old_user[i]):
            del(user_list[j])
            break
print(len(user_list))



for i in range(len(user_list)):
    infor={}
    num=0
    to =[]
    for j in range(len(json_data)):
        if(num<=40):
            if(json_data[j]['user_id']==user_list[i]):
                try:
                    if(0<len(json_data[j]['content'])<300):
                        print(weibo_filter(json_data[j]['content']))
                        sys.stdout.flush()
                        if('抑郁' in json_data[j]['content'] or '吃药' in json_data[j]['content']):
                            num+=1
                            to.append(weibo_filter(json_data[j]['content']))
                    else:
                        continue
                except:
                    print("2")
                    continue
                else:
                    continue
            else:
                continue
        else:
            break
    try:
        print("########################################################################################")
        print(to)
        print('Total number:',num)
    except:
        continue
    try:
        tag = input('Please input tag :')
    except:
        tag='0'
    try:
        infor[str(user_list[i])]=str(tag)
        with open(r'C:\Users\12068\Desktop\black_users\new_black_tag.json',mode='a',encoding='utf_8') as file1:
            json.dump(infor,file1,indent=4)
        sys.stdout.flush()
    except:
        print('error')
