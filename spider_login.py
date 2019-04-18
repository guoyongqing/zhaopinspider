#!/usr/bin/python

import requests
import random
import time
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
import re


# 登陆URL
LOGIN_URL = 'https://accounts.douban.com/j/mobile/login/basic'

# 个人主页URL
PEOPLE_URL = 'https://www.douban.com/people/'

# 账号信息
user = {
    'username':'13262953685',
    'password':'abc123456'
}


# 加载User-Agent
def load_user_agents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1]) #去掉换行
    random.shuffle(uas)
    return uas


# 伪装成浏览器请求
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

# 代理（免费代理：http://www.goubanjia.com/）
proxies = {
    'http': '182.52.238.52:50619',
    'http': '95.31.197.77:41651',
    'http': '119.180.179.71:8060',
}

time1 = time.time()


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


# 抓取个人主页
def get_source(url):
    r = requests \
        .session() \
        .get(url,
                headers=query_head,
                proxies=proxies
                ) \
        .text
    find_interested_groups(r)


groups = []


# 查找"我常去的小组"
def find_interested_groups(html_doc):
    soup = BeautifulSoup(html_doc,'lxml')
    print(soup.prettify() + '\n\n********************************************************')
    # 找出文本内容包含'我常去的小组'的所有h2标签
    groups_h2 = soup.find_all('h2',string=re.compile('我常去的小组'))[0]
    # 找到其后所有的兄弟dl节点
    dl_siblings = groups_h2.find_next_siblings()
    dd = dl_siblings.dd
    a = dd.a
    group = a.string.strip()[:-1]
    groups.append(group)
    print('groups : ' + groups + '\n\n********************************************************')


urls = []

# 抓取并解析100个用户数据，保存
for m in range(59798134, 59798235):
    url = PEOPLE_URL + str(m)
    urls.append(url)


# 程序入口
if __name__ == "__main__":
    pool = ThreadPool(1)
    login(LOGIN_URL,user['username'],user['password'])
    try:
        results = pool.map(get_source, urls)
    except Exception as e:
        print(e)

    pool.close()
    pool.join()