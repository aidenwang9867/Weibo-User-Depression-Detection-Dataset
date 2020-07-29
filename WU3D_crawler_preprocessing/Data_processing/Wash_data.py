import json
import pandas as pd
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


with open(r'C:\Users\12068\Desktop\black_users\5.20_black.json', 'r', encoding='utf_8') as f:
    json_data = json.load(f)

for i in range(len(json_data)):
    del_list=[]
    print(i)
    for j in range(len(json_data[i]['infor'])):
        if('此微博已不可见' in json_data[i]['infor'][j]['Context'] or '被作者删除' in json_data[i]['infor'][j]['Context']):
            del_list.append(json_data[i]['infor'][j]['Context'])
        else:
            if(json_data[i]['infor'][j]['Self'] == 'True'):
                one_info = json_data[i]['infor'][j]['Context']
                new_one_info = one_info.replace('原图', '')
                new_one_info = new_one_info.replace('显示地图', '')
                new_one_info = new_one_info.replace('地图', '')
                new_one_info = new_one_info.replace('显示地图', '')
                # abandon URL
                new_one_info = re.sub(
                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', new_one_info)
                # abandon
                new_one_info = re.sub('\[共\d*?张]', '', new_one_info)
                #abandon #
                new_one_info = re.sub('\【(.*)】', '', new_one_info)
                #abandon #
                new_one_info = re.sub('\#.*\#', '', new_one_info)
                # abandon //@
                new_one_info = re.sub('\[组图共\d*?张\]', '', new_one_info)
                new_one_info = new_one_info.replace('组图', '')
                new_one_info = re.sub('//@.*?:', ' ', new_one_info)
                new_one_info = re.sub('(\s)([^\s])*?的微博视频', '', new_one_info)
                new_one_info = re.sub(
                    '(\s)([^\s])*?·([^\s])*', '', new_one_info)
                # abandon
                new_one_info = new_one_info.replace('分享图片', '')
                new_one_info = new_one_info.replace('(@网易云音乐)', '')
                new_one_info = new_one_info.replace('查看图片', '')
                if (new_one_info.isspace() == True or len(new_one_info) == 0):
                    new_one_info = '无'
                json_data[i]['infor'][j]['Context']=weibo_filter(new_one_info)
            elif(json_data[i]['infor'][j]['Self'] == 'False'):
                one_info = json_data[i]['infor'][j]['Context']
                try:
                    new_one_info = re.findall('转发理由:.*', one_info)[0]
                except:
                    continue
                new_one_info = new_one_info.replace("转发理由:", '')
                new_one_info = new_one_info.replace('原图', '')
                new_one_info = new_one_info.replace('转发微博', '')
                new_one_info = new_one_info.replace('显示地图', '')
                # abandon URL
                new_one_info = re.sub(
                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', new_one_info)
                # abandon
                new_one_info = re.sub('\[共[0-9]*张]', '', new_one_info)
                #abandon #
                new_one_info = re.sub('\【(.*)】', '', new_one_info)
                # abandon //@
                new_one_info = re.sub('//@.*?:', ' ', new_one_info)
                # abandon []
                new_one_info = re.sub('\[组图共\d*?张\]', '', new_one_info)
                new_one_info = new_one_info.replace('组图', '')
                #abandon #
                new_one_info = re.sub('\#.*\#', '', new_one_info)
                new_one_info = re.sub('(\s)([^\s])*?的微博视频', '', new_one_info)
                new_one_info = re.sub(
                    '(\s)([^\s])*?·([^\s])*', '', new_one_info)
                new_one_info = new_one_info.replace('分享图片', '')
                new_one_info = new_one_info.replace('(@网易云音乐)', '')
                new_one_info = new_one_info.replace('查看图片', '')
                if (new_one_info.isspace() == True or len(new_one_info) == 0):
                        new_one_info = '无'
                json_data[i]['infor'][j]['Context']=weibo_filter(new_one_info)
            else:
                continue
            
    for m in range(len(del_list)):
        for n in range(len(json_data[i]['infor'])):
            if json_data[i]['infor'][n]['Context']==del_list[m]:
                del(json_data[i]['infor'][n])
                break
            else:
                continue


with open(r'C:\Users\12068\Desktop\black_users\5.22.json','w',encoding='utf_8') as f3:
    json.dump(json_data,f3,ensure_ascii=False)


