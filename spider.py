import requests


url = 'https://www.douban.com/people/59798134/'

try:
    r = requests.post(url, timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text)  # 部分信息
except:
    print("失败")