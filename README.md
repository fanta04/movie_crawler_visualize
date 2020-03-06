# 爬取和分析豆瓣电影短评页面（好评差评词云，用户注册时间，评论增长曲线）
本项目以电影《寄生虫》为例，爬取豆瓣电影短评页面五星、三星、一星共1500条评论

## 主要文件为：

 - fetch.py实现爬取，页面解析，存储到数据库 
 - visual.py实现词云绘制，好评差评用户注册时间对比，评论增长曲线
 - stopwords.txt停用词表

## 用到的工具库有：

 - requests 
 - BeautifulSoup
 -  pymysql 
 - jieba 
 - numpy 
 - pandas 
 - pyecharts

## 好评差评都在说什么
![image](https://github.com/fanta04/movie_crawler_visualize/blob/master/Image/good_comment.JPG)
![image](https://github.com/fanta04/movie_crawler_visualize/blob/master/Image/bad_comment.JPG)
## 评论增长曲线
![image](https://github.com/fanta04/movie_crawler_visualize/blob/master/Image/comment_line.png)
## 用户注册时间对比
![image](https://github.com/fanta04/movie_crawler_visualize/blob/master/Image/register_time.jpg)
