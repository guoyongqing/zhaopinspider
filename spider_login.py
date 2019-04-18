#!/usr/bin/python

import requests
import random
import time
from bs4 import BeautifulSoup
import re
import numpy as np
import write_excel


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


# 执行爬数据
def do_spider():
    index = 0
    # 失败重试次数（最大设置为10）
    try_times = 0
    list = []
    while (index < len(urls)):
        url = urls[index]
        # 模拟等待延时
        time.sleep(np.random.rand() * 5)
        try:
            r = requests \
                .session() \
                .get(url,
                     headers=query_head,
                     proxies=proxies,
                     timeout=30
                     ) \
                .text
        except:
            continue

        # 一条用户信息
        userid = url[-8]
        groups = []
        soup = BeautifulSoup(r, 'lxml')
        print(soup.prettify() + '\n\n********************************************************')
        # 找出文本内容包含'我常去的小组'的所有h2标签
        groups_h2 = soup.find('h2', string=re.compile('常去的小组'))
        try_times += 1
        if groups_h2 == None and try_times < 10:
            continue
        elif groups_h2 == None or len(groups_h2) <= 1:
            break

        nickname = soup.title.string
        # 找到其后所有的兄弟dl节点
        dl_siblings = groups_h2.find_next_siblings()
        for dl in dl_siblings:
            dd = dl.dd
            a = dd.a
            groupname = a.string.strip()[:-1]
            link = a.get('href')
            group = [userid, nickname, groupname, link]
            groups.append(group)
        print('groups : ' + groups + '\n\n********************************************************')
        index += 1
        list.append(groups)
    return list


# 保存数据到excel
def save_data_to_excel(list):
    write_excel.write_excel_row(list)


urls = []

# 随机抓取并解析1000个用户数据，保存
for m in range(59798134, 59798135):
    url = PEOPLE_URL + str(m)
    urls.append(url)


# 程序入口
if __name__ == "__main__":
    # 模拟登陆
    login(LOGIN_URL,user['username'],user['password'])
    # 爬取数据
    group_list = do_spider()
    # 保存数据
    save_data_to_excel(group_list)