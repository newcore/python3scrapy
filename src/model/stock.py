from urllib import request
import random
import time

import pymysql
from bs4 import BeautifulSoup
from search_engines.functions import db_Model

class stock():
    __db = None
    def __init__(self):
        self.__db = db_Model()

    #下载股票信息
    def download_stocks(self):
        self.download_pages()  # 下载页面
        stocks = self.get_stocks()  # 获取股票页面
        self.add_stock_item(stocks)  # 添加股票最新信息
        self.update_stocks()  # 更新股票的操作情况

    def get_content(self,url):
        user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
                      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                      'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                      'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                      'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                      'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

        try:
            req = request.Request(url,headers={"User-Agent":random.choice(user_agent)})
            respons = request.urlopen(req)
            content = respons.read().decode('gbk', 'ignore')
            content = content.encode('utf-8').decode('utf-8')
            print('get page : %s' % url)
            now = time.strftime('%Y-%m-%d',time.localtime())
            data = {'page_url':url,'content':pymysql.escape_string(content),'created':now}
            self.__db.table('pages').insert(data)
            # conn = get_conn()
            # cursor = conn.cursor()
            #
            # insert_sql = "insert into pages (page_url,content,created) VALUES ('%s','%s','%s')" % (url, pymysql.escape_string(content),now)
            # cursor.execute(insert_sql)
            # conn.commit()
            # cursor.close()
            # conn.close()
        except Exception as e:
            print(e)

    def download_pages (self) :
        for i in range(1, 110):
            url = 'http://quote.stockstar.com/stock/ranklist_a_3_1_' + str(i) + '.html'  # 目标网址
            self.get_content(url)

    def get_stocks(self):
        sql = 'select * from pages where operate  = 0 '
        data = self.__db.query(sql)
        return data


    def update_stocks(self):
        sql = 'update pages set operate = 1 where operate  = 0 '
        self.__db.execute(sql)


    def add_stock_item(self,stocks):
        date = time.strftime('%Y-%m-%d',time.localtime())
        count = 0
        for row in stocks :
            soup = BeautifulSoup(row['content'],'html.parser')
            trs = soup.find('tbody',id='datalist').find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                stock_data = []
                for td in tds :
                    stock_data.append(td.get_text())
                insert_sql = "insert into stock_items (stock_no,name,price,up_down_rate,up_down_price,min5_up_down,volume,turnover,turnover_rate,amplitude,volume_ratio,committee,pe_ratio,date) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (stock_data[0],stock_data[1],stock_data[2],stock_data[3],stock_data[4],stock_data[5],stock_data[6],stock_data[7],stock_data[8],stock_data[9],stock_data[10],stock_data[11],stock_data[12],date)
                self.__db.execute(insert_sql)
                count = count + 1
                print("ID of last record is %d ,count %d" % (int(self.__db.get_last_insert_id()), count))  # 最后插入行的主键ID


