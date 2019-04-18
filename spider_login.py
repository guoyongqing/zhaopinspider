#!/usr/bin/python

import requests
import json
import random
import pymysql
import datetime
import time
from multiprocessing.dummy import Pool as ThreadPool


# 登陆URL
LOGIN_URL = 'https://accounts.douban.com/j/mobile/login/basic'

# 个人主页URL
PEOPLE_URL = 'https://www.douban.com/people/'


user = {
    'username':'13262953685',
    'password':'shadeless.1990'
}


# 日期转换成毫秒
def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))
    return current_milli_time()


# 加载User-Agent
def load_user_agents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas


uas = load_user_agents("user_agents.txt")

# 请求头（模拟浏览器登陆）
login_head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://accounts.douban.com/passport/login',
    'Origin': 'https://accounts.douban.com',
    'Host': 'accounts.douban.com',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'application/json',
}

# 请求头（查询个人主页）
query_head = {
    'User-Agent': random.choice(uas), # 随机取值
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://accounts.douban.com/passport/login',
    'Origin': 'https://accounts.douban.com',
    'Host': 'www.douban.com',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
}


# 代理
proxies = {
    'http': 'http://120.26.110.59:8080',
    'http': 'http://120.52.32.46:80',
    'http': 'http://218.85.133.62:80',
}

time1 = time.time()


# # 登录
# def login(baseurl,username,password):
# 　　# 使用seesion登录，保留登录信息
#     session = requests.session()
# 　　#登录的URL
#     baseurl += "/login/email"
# 　　#requests 的session登录，以post方式，参数分别为url、headers、data
#     content = session.post(baseurl, headers = headers_base, data = login_data)
# 　　#成功登录后输出为 {"r":0,
# 　　#"msg": "\u767b\u9646\u6210\u529f"
# 　　#}
#     print content.text
# 　　#再次使用session以get去访问知乎首页，一定要设置verify = False，否则会访问失败
#     s = session.get("http://www.zhihu.com", verify = False)
#     print s.text.encode('utf-8')
# 　　#把爬下来的知乎首页写到文本中
#     f = open('zhihu.txt', 'w')
#     f.write(s.text.encode('utf-8'))


# 登陆
def login(baseurl,username,password):
    # form data
    payload = {
        'ck': '',
        'name': username,
        'password': password,
        'remember': False,
        'ticket': ''
    }
    r = requests.session().post(baseurl, headers=login_head, data=payload, timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text + '\n\n********************************************************')


urls = []

# 抓取并解析数据，保存
for m in range(59798134, 59798145):
    url = PEOPLE_URL + str(m)
    urls.append(url)


    def get_source(url):
        r = requests \
            .session() \
            .get(PEOPLE_URL,
                  headers=query_head,
                  # proxies=proxies
                 ) \
            .text



if __name__ == "__main__":
    pool = ThreadPool(1)
    login(LOGIN_URL,user['username'],user['password'])
    try:
        results = pool.map(get_source, urls)
    except Exception as e:
        print(e)

    pool.close()
    pool.join()