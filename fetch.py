# noinspection PyUnresolvedReferences
import requests
from lxml import etree
from bs4 import BeautifulSoup
import pymysql
import time
import  random

postIds = []
uids = []
times = []
agrees = []
stars = []
comments = []
regtimes = []
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': ''
          }

def get_page(url):
    html = requests.get(url,headers = header).text
    return html

def parse4data(html):
    soup = BeautifulSoup(html,"lxml")
    ids = soup.select('.comment-item')
    for tag in ids:
        #根据用户头像链接抓取用户注册时间
        # userinfo = tag.find(class_ = 'avatar').find('a')['href']
        # url = requests.get(userinfo,headers = header).content
        # s = BeautifulSoup(url,"lxml")
        # #print(userinfo)
        # try:
        #     reg = s.find(class_ = 'user-info')
        #     regtime = reg.find(class_ = "pl").get_text().split('  ')[1][:4]
        #     regtimes.append(regtime)
        # except AttributeError:
        #     regtimes.append('null')

        #抓取用户ID，赞同数，用户昵称，发布时间，详细评论
        postId = tag['data-cid']
        agree = tag.find(class_ = 'votes').string
        info = tag.select('.comment-info')
        for u in info:
            uid = u.find('a').string
            time = u.find(class_ = 'comment-time')['title']
            uids.append(uid)
            times.append(time)
        comment = tag.find(class_ = 'short').string

        postIds.append(postId)
        agrees.append(agree)
        comments.append(comment)

#把数据存入mysql数据库
def save4mysql(movieid,level):
    #douban数据库是提前建好的
    db = pymysql.connect(host='localhost',user='',password='',database='douban',autocommit = 'True',charset='utf8mb4')
    cursor = db.cursor()
    print("connect OK!")
    table_name = movieid+level
    sql = '''create table %s(
                id int primary key not null,
                postId varchar(50),
                uid varchar(50), 
                postTime varchar(50), 
                agree varchar(50),
                comment text)'''
    cursor.execute(sql %table_name)     #建表
    convert = 'alter table %s convert to character set utf8mb4 collate utf8mb4_bin' % (table_name)
    cursor.execute(convert)
    print('Create table OK!')
    for i in range(len(postIds)):
        inssql = """insert into %s (id,postId,uid,postTime,agree,comment)\
                                values (%d,"%s","%s","%s","%s","%s")""" \
                 % (table_name, i, postIds[i], uids[i], times[i], agrees[i],
                    pymysql.escape_string(comments[i]))
        cursor.execute(inssql)
        # print('insert succ!')

if __name__ == '__main__':
    cnt = 0
    types = 'l'              #type值为h-五星，m-三星，l-一星
    movieid = '27010768'     #以寄生虫的电影编号为例
    base_url = 'https://movie.douban.com/subject/27010768/comments?start='+str(cnt)+'&limit=20&sort=new_score&status=P&percent_type='
    link = base_url
    print('Start')
    #豆瓣评论每页20条，每类评论总共可查看500条
    while(cnt<=480):
        link = 'https://movie.douban.com/subject/27010768/comments?start=' + str(cnt) + '&limit=20&sort=new_score&status=P&percent_type='
        html = get_page(link + types)
        parse4data(html)
        print("Processing "+link+types+"...")
        cnt += 20
        time.sleep(random.random())
    save4mysql(movieid,types)
    postIds.clear()
    uids.clear()
    times.clear()
    agrees.clear()
    stars.clear()
    comments.clear()
    regtimes.clear()

    print('End')








