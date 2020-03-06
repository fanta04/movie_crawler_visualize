#-*-coding:utf-8-*-
import pymysql
import jieba
import numpy as np
import pandas
import matplotlib.pyplot as plt
import PIL
import wordcloud
import io
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts

#连接数据库
def connect_to_mysql(table_name):
    conn = pymysql.connect(host = 'localhost',user = '',password = '',database = 'douban',charset = 'utf8')
    cursor = conn.cursor()
    sql = 'select * from %s'%(table_name)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

#转化成DataFrame，清洗数据
def get_data(res):
    col = ['id','postId','uid','postTime','agree','comment']
    df = pandas.DataFrame(list(res),columns=col)
    df = df.drop_duplicates(subset='postId')  #删掉postId重复的用户
    df['postTime'] = df['postTime'].str[0:10]            #统一评论发布时间的格式
    #df = df[~df['regTime'].isin(['null'])]    #删掉不存在的用户
    #df['regTime'] = df['regTime'].astype(int)
    return df

def get_comment_line(df1,df2,df3):
    #整合三个表的数据
    df = df1.append(df2)
    df = df.append(df3)

    #按照时间排序
    res = df['postTime'].value_counts().sort_index()

    values = []
    date = []
    for v in res.values:
        values.append(int(v))
    for v in res.index:
        date.append(str(v))

    #生成折线图
    line = Line()
    line.add_xaxis(date)
    line.add_yaxis("评论数",values,is_smooth=True,areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.set_global_opts(title_opts=opts.TitleOpts(title="每日评论数走势图"))
    line.render(path = 'comment_line.html')

#绘制影评词云
def draw_wordcloud(df,name):
    segment = []
    #打开停用词表
    stopwords = [line.strip() for line in
                 io.open('stopwords.txt', 'r', encoding='utf-8').readlines()]

    for comment in df['comment']:
        words = jieba.cut(comment)
        for word in words:
            #去停用词
            if word not in stopwords and word !=' ' and word !='\n':
                segment.append(word)
    #统计词频
    dfword = pandas.Series(segment)
    dfword = dfword.value_counts()
    dfword.to_dict()

    #绘制词云
    img = PIL.Image.open("father.JPG")
    grp = np.array(img)
    wc = wordcloud.WordCloud(
        background_color="white",
        max_words=100,
        font_path="SIMYOU.TTF",
        mask = grp,
        width=400
    )
    wc.generate_from_frequencies(dfword)
    wc.to_file("%s_comment.JPG"%name)

def draw_regtime_bar(good,bad):
    good = good['regTime'].value_counts().sort_index()
    bad = bad['regTime'].value_counts().sort_index()
    bar = Bar()
    values1 = []
    values2 = []
    for v in good.values:
        values1.append(int(v))
    for v in bad.values:
        values2.append(int(v))
    bar.add_xaxis(list(good.index))
    bar.add_yaxis('好评用户注册年份',values1)
    bar.add_yaxis('差评用户注册年份', values2)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="好评用户注册时间"))
    bar.render()

if __name__ == '__main__':
    movieid = '27010768'
    typeh = 'h'
    typem = 'm'
    typel = 'l'
    resh = connect_to_mysql(movieid + typeh)
    resm = connect_to_mysql(movieid + typem)
    resl = connect_to_mysql(movieid + typel)
    df1 = get_data(resh)
    df2 = get_data(resm)
    df3 = get_data(resl)
    get_comment_line(df1,df2,df3)
    draw_wordcloud(df1,'good')
    draw_wordcloud(df3,'bad')
    # draw_regtime_bar(good,bad)