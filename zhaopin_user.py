# -*-coding:utf8-*-

import requests
import json
import random
import pymysql
import sys
import datetime
import time
from imp import reload
from multiprocessing.dummy import Pool as ThreadPool


# 日期转换成毫秒
def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))
    return current_milli_time()


reload(sys)


def load_user_agents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas


uas = load_user_agents("user_agents.txt")

head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

# Please replace your own proxies.
proxies = {
    'http': 'http://120.26.110.59:8080',
    'http': 'http://120.52.32.46:80',
    'http': 'http://218.85.133.62:80',
}

time1 = time.time()

urls = []

# Please change the range data by yourself.
for m in range(5214, 5215):
    for i in range(m * 100, (m + 1) * 100):
        url = 'https://space.bilibili.com/' + str(i)
        urls.append(url)


    def get_source(url):
        payload = {
            '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
            'mid': url.replace('https://space.bilibili.com/', '')
        }
        ua = random.choice(uas)
        head = {
            'User-Agent': ua,
            'Referer': 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(random.randint(10000, 50000))
        }
        jscontent = requests \
            .session() \
            .post('http://space.bilibili.com/ajax/member/GetInfo',
                  headers=head,
                  data=payload,
                  proxies=proxies) \
            .text
        time2 = time.time()
        try:
            js_dict = json.loads(jscontent)
            status_json = js_dict['status'] if 'status' in js_dict.keys() else False
            if status_json:
                if 'data' in js_dict.keys():
                    js_data = js_dict['data']
                    mid = js_data['mid']
                    name = js_data['name']
                    sex = js_data['sex']
                    rank = js_data['rank']
                    face = js_data['face']
                    reg_time_stamp = js_data['regtime']
                    reg_time_local = time.localtime(reg_time_stamp)
                    reg_time = time.strftime("%Y-%m-%d %H:%M:%S", reg_time_local)
                    spacesta = js_data['spacesta']
                    birthday = js_data['birthday'] if 'birthday' in js_data.keys() else 'nobirthday'
                    sign = js_data['sign']
                    level = js_data['level_info']['current_level']
                    official_verify_type = js_data['official_verify']['type']
                    OfficialVerifyDesc = js_data['official_verify']['desc']
                    vipType = js_data['vip']['vipType']
                    vipStatus = js_data['vip']['vipStatus']
                    toutu = js_data['toutu']
                    toutuId = js_data['toutuId']
                    coins = js_data['coins']
                    print("Succeed get user info: " + str(mid) + "\t" + str(time2 - time1))
                    try:
                        res = requests.get(
                            'https://api.bilibili.com/x/relation/stat?vmid=' + str(mid) + '&jsonp=jsonp').text
                        viewinfo = requests.get(
                            'https://api.bilibili.com/x/space/upstat?mid=' + str(mid) + '&jsonp=jsonp').text
                        js_fans_data = json.loads(res)
                        js_viewdata = json.loads(viewinfo)
                        following = js_fans_data['data']['following']
                        fans = js_fans_data['data']['follower']
                        archiveview = js_viewdata['data']['archive']['view']
                        article = js_viewdata['data']['article']['view']
                    except:
                        following = 0
                        fans = 0
                        archiveview = 0
                        article = 0
                else:
                    print('no data now')
                try:
                    # 连接database
                    conn = pymysql.connect(
                        host='localhost', user='root', passwd='123456', db='bilibili', charset='utf8')
                    # 得到一个可以执行sql语句的光标对象，执行返回的结果集默认以元组显示
                    cur = conn.cursor()
                    cur.execute('INSERT INTO bilibili_user_info(mid, name, sex, rank, face, reg_time, spacesta, \
                                birthday, sign, level, official_verify_type, OfficialVerifyDesc, vipType, vipStatus, \
                                toutu, toutuId, coins, following, fans ,archiveview, article) \
                    VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",\
                            "%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s")'
                                %
                                (mid, name, sex, rank, face, reg_time, spacesta, \
                                 birthday, sign, level, official_verify_type, OfficialVerifyDesc, vipType, vipStatus, \
                                 toutu, toutuId, coins, following, fans, archiveview, article))
                    conn.commit()
                except Exception as e:
                    print(e)
            else:
                print("Error: " + url)
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    pool = ThreadPool(1)
    try:
        results = pool.map(get_source, urls)
    except Exception as e:
        print(e)

    pool.close()
    pool.join()
