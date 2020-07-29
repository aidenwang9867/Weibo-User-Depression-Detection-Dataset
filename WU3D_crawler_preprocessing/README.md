# Weibo_Spider
爬虫有两个版本，早期使用的版本和后期使用的版本:
## Weibo_Spider1.0：
- 配置topic_config.json,里面集合了对超话爬虫的配置并设置数据对应的输出格式
- 运行topic_spider.py,针对超话爬虫的主体部分，按照config设置输出对应数据
- 配置user_config.json,集合了对用户爬虫的配置
- 运行user_spider.py,针对爬虫的主体部分，按照设置，对特定ID用户进行信息爬取并按照规定格式输出

|Name|Function|
|:---:|:---:|
|topic_config.json|针对超话爬虫的一些设置（包括超话名称、爬取时间范围和数据输出格式等）|
|topic_spider.py|超话爬虫的主体部分|
|user_config.json|针对用户爬虫的一些设置（包括爬取用户ID、时间范围和数据输出格式等）|
|运行user_spider.py|用户爬虫的主体部分|


## Weibo_Spider2.0:
需要配置在Docker平台上
### 版本说明
该项目分为2个分支，以满足不同的需要

|分支|特点|抓取量|
|:---:|:---:|:---:|
|simple|单账号,单IP,单机器|十万级|
|master|账号池,IP池,Docker分布式|数亿级(**理论无上限**)|

### 支持爬虫
- 用户信息抓取
- 用户微博抓取
- 用户社交关系抓取(粉丝/关注)
- 微博评论抓取
- 基于关键词和时间段的微博抓取

### 如何使用
#### 拉取镜像

```bash
docker pull portainer/portainer
docker pull mongo
docker pull mongo-express
docker pull redis
docker pull registry.cn-hangzhou.aliyuncs.com/weibospider/account
docker pull registry.cn-hangzhou.aliyuncs.com/weibospider/spider
```

#### 启动项目
```bash
docker stack deploy -c <(docker-compose config) weibospider
```

```bash
docker service ls 
-----------------
ID                  NAME                               MODE                REPLICAS            IMAGE                                                          PORTS
f7yx1cjh1izt        weibospider_portainer              replicated          1/1                 portainer/portainer:latest                                     *:7000->9000/tcp
5szekv996su0        weibospider_mongodb                replicated          1/1                 mongo:latest                                                   *:7001->27017/tcp
lq7kmlekcrlg        weibospider_mongo-express          replicated          1/1                 mongo-express:latest                                           *:7002->8081/tcp
xjbddlf53hai        weibospider_redis                  replicated          1/1                 redis:latest                                                   *:7003->6379/tcp
mk8dmh6nl17i        weibospider_account                replicated          1/1                 registry.cn-hangzhou.aliyuncs.com/weibospider/account:latest
nvo9dt0r5v2t        weibospider_weibo-spider-comment   replicated          1/1                 registry.cn-hangzhou.aliyuncs.com/weibospider/spider:latest
vbnyacpm3xle        weibospider_weibo-spider-fan       replicated          1/1                 registry.cn-hangzhou.aliyuncs.com/weibospider/spider:latest
qyvu9wt0fzny        weibospider_weibo-spider-follow    replicated          1/1                 registry.cn-hangzhou.aliyuncs.com/weibospider/spider:latest
h3dfh8qr1eak        weibospider_weibo-spider-tweet     replicated          1/1                 registry.cn-hangzhou.aliyuncs.com/weibospider/spider:latest
jiaz176hzbls        weibospider_weibo-spider-user      replicated          1/1                 registry.cn-hangzhou.aliyuncs.com/weibospider/spider:latest
```
- portainer http://127.0.0.1:7000 

通过portainer可以方便得对所有的服务进行管理,查看服务状态，运行日志。

通过`scale`可快速进行服务的启动(置为1)，停止(置为0)，扩容(比如，置为100)

- mongo-express http://127.0.0.1:7002

通过mongo-express可以方便得查看管理mongo数据库



#### 构建账号池
**准备无验证码类型的微博小号**

将购买的小号填充到`./weibospider/account/account.txt`，格式与`./weibospider/account/account_sample.txt`保持一致。

获取容器id，并进入容器
```bash
docker container ls | grep weibospider_account
1f15415443f8        registry.cn-hangzhou.aliyuncs.com/weibospider/account:latest   "python3"                22 minutes ago      Up 22 minutes                           weibospider_account.1.h091uc5sm0l1iz9oxpa7ypwak

docker exec -it 1f15415443f8 bash
root@1f15415443f8:/app#
```

构建账号池
```bash
root@1f15415443f8:/app# cd account
root@1f15415443f8:/app# python login.py
2020-04-15 11:56:56 ==============================
2020-04-15 11:56:56 start fetching cookie [zhanyuanben85c@163.com]
2020-04-15 11:57:04 cookie: _T_WM=0bfd51e7d3bdc1f914c5dbce3a4b20e0; SSOLoginState=1586923020; SUHB=010GS1NzSA-zOR; SCF=AmfAT-ydYBWL_ip0UMdV5KYFRwiWaFNTPoxWBgCc76c8PHXBkcp-CSNZArDRyyt1oShEm-T4Qukkw9W9n5eGrXA.; SUB=_2A25zkvZcDeRhGeFN71AY9i7FyzuIHXVRfJoUrDV6PUJbkdANLXjTkW1NQDAS-yKGeo_seRGTTKVAeOs1IG_ucher
2020-04-15 11:57:04 ==============================
2020-04-15 11:57:04 start fetching cookie [chuicong7188031104@163.com]
2020-04-15 11:57:11 cookie: _T_WM=6cf59fb4e2df7ba2b15e93d6bc184940; SSOLoginState=1586923028; SUHB=06ZV1_UTgTUirk; SCF=AvGBrUc4rNRZapeLXnQjOvrK9SyaN8dtGH_JfZamRkCRwCC6H1NJmJ6EVdZG26_lwfURJ233mRb5G-ZiM3WgGWA.; SUB=_2A25zkvZEDeRhGeFN71ET9S_Fzj6IHXVRfJoMrDV6PUJbkdANLRahkW1NQDAPyyhLB1NH_XSKtFoOQ2xwxkKWEMh5
2020-04-15 11:57:11 ==============================
2020-04-15 11:57:11 start fetching cookie [zhi21614055@163.com]
2020-04-15 11:57:19 cookie: _T_WM=6cc104aff523785aed114eb28996cb84; SSOLoginState=1586923035; SUHB=0bts1yfOjc42hI; SCF=AtAdd0uPAxdek8Hhh6JBOkxqFANmv7EqVebH6aHdY-3T_LUHoaIp6TaCo_57zCFZ-izJVcs01qs20b5cBpuwS_c.; SUB=_2A25zkvZLDeRhGeFN71AY9CjLwjuIHXVRfJoDrDV6PUJbkdANLWXjkW1NQDAJWlhRm6NkHCqHoOG9PBE1DOsaqX39
```


#### 初始化Redis

```bash
root@be3ac5910132:/app# python redis_init.py <arg>
```
参数arg可选项为:
- `user`: 初始化用户信息爬虫队列，对应`weibospider_weibo-spider-user`docker服务
- `fan`: 初始化用户粉丝列表爬虫队列，对应`weibospider_weibo-spider-fan`docker服务
- `follow`: 初始化用户关注列表爬虫队列，对应`weibospider_weibo-spider-follow`docker服务
- `comment`: 初始化微博评论爬虫队列，对应`weibospider_weibo-spider-comment`docker服务
- `tweet_by_user_id`: 初始化用户微博爬虫队列，对应`weibospider_weibo-spider-tweet`docker服务
- `tweet_by_keyword`: 初始化基于关键词和时间端的微博爬虫队列，对应`weibospider_weibo-spider-tweet`docker服务

可根据自己的需求自行修改`./weibospider/redis_init.py`

下面以`tweet_by_user_id`为例
```bash
root@be3ac5910132:/app# python redis_init.py tweet_by_user_id
Add urls to tweet_spider:start_urls
Added: https://weibo.cn/1087770692/profile?page=1
Added: https://weibo.cn/1699432410/profile?page=1
Added: https://weibo.cn/1266321801/profile?page=1
```


# Data_processing
## 功能说明
|Name|Function|
|:---:|:---:|
|Tag.py|对获取的数据进行人工标注|
|Deal_csv.py|将Spider1.0输出csv格式的数据输出为需要的json格式数据|
|UID_to_name.py|将微博的微号转换为用户的ID及昵称|
|Data_conversion.py|将Spider2.0输出json格式的数据输出为需要的json格式数据|
|Wash_data.py|将得到的数据进行清洗（去掉冗余的信息）|
|Get_pic.py|根据URL获取图片|

## 最终数据格式
```bash
{
    "User":"用户昵称"
    "ID"："用户ID"
    "Sex":"性别"
    "Birth":"生日"
    "Number of fans":粉丝数量
    "Micro-blog number": 微博数
    "Concern number"：关注数
    "brief introduction":个人简介
    "infor":{
        有多条用户博文
        [
            "Context":微博正文
            "time":发布时间
            "Thumb-UP":点赞数
            "Comment":评论数
            "Forward":转发数
            "Self": 是否为自制
        ]
        ........
    }
    "Original Count"：原创博文数
    "Reprint Count:"：转发博文数
}
```


