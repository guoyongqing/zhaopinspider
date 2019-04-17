import requests
import json


# url = 'https://www.douban.com/people/59798134/'
# try:
#     r = requests.post(url, timeout=30)
#     r.raise_for_status()
#     r.encoding = r.apparent_encoding
#     print(r.text)  # 部分信息
# except:
#     print("失败")



# 登陆URL
url = 'https://accounts.douban.com/j/mobile/login/basic'

# 目标URL
url1 = 'https://www.douban.com/people/59798134/'

# 请求头（模拟浏览器访问）
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://accounts.douban.com/passport/login',
    'Origin': 'https://accounts.douban.com',
    'Host': 'accounts.douban.com',
    # 'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'application/json',
}

head1 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://accounts.douban.com/passport/login',
    'Origin': 'https://accounts.douban.com',
    'Host': 'www.douban.com',
    # 'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
}

# form data
payload = {
    'ck': '',
    'name': '13262953685',
    'password': 'shadeless.1990',
    'remember': False,
    'ticket': ''
}

try:
    session = requests.session()
    r = session.post(url,headers=head,data=payload,timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text + '\n\n********************************************************')

    r = session.get(url1,headers=head1,timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text)
except:
    print("失败")