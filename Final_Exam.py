import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd

ua = UserAgent()
header = {'User-Agent': ua.random}

user_name = []
rate = []
time = []
com = []
vote = []

for start in range(0, 41, 20): # start参数分别为0, 20, 40, 对应第1、2、3页
    url = f'https://movie.douban.com/subject/35288767/comments?percent_type=&start={start}&limit=20&status=P&sort=new_score&comments_only=1'

    response = requests.get(url=url, headers=header)
    a = response.json()
    soup = BeautifulSoup(a['html'], 'lxml')

    avatar = soup.find_all(name='div', attrs={"class": "avatar"})
    for i in avatar:
        user_name.append(i.a["title"])

    rating = soup.find_all(name='span', attrs={"class": "rating"})
    for i in rating:
        rate.append(i["class"][0][-2:-1])

    comment_time = soup.find_all(name='span', attrs={"class": "comment-time"})
    for i in comment_time:
        time.append(i["title"][:-9])

    comment = soup.find_all(name='span', attrs={"class": "short"})
    for i in comment:
        com.append(i.text)

    votes = soup.find_all(name='span', attrs={"class": "votes"})
    for i in votes:
        vote.append(i.text)

df = pd.DataFrame({"用户名": user_name, "评分": rate, "发表时间": time, "短评正文": com, "赞同数量": vote})
df.to_csv('result.csv', encoding='utf_8_sig')
