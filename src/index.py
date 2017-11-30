# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, request
import sys
sys.path.insert(0,'..')
from search_engines.model.stock import stock
from search_engines.utils.page import page
from search_engines.functions import *


app = Flask(__name__)

@app.route('/')
def index() :
    stock_list = db_Model().query('select * from stock ORDER BY rand() limit 7')
    return render_template('index.html',stock_list=stock_list)

@app.route('/s')
def search() :
    q = request.args.get('q','')
    current_page = request.args.get('page',1)
    try:
        dbModel = db_Model()
        keywords = '%'+q+'%'
        sql = 'select * from stock s left join stock_items item on s.stock_no = item.stock_no where s.stock_no like "%s" or s.name like "%s"  order by item.date desc ' % (keywords,keywords)
        total_data_count = dbModel.count(sql)
        page_size = 10
        offset = str((int(current_page)-1)*int(page_size))
        stock_list = dbModel.query(sql + ' limit %s,%s' % (offset,str(page_size)))
        pageModel = page(total_data_count,current_page=int(current_page),page_size = int(page_size), page_url='http://so.izelu.com')
        page_info = pageModel.show()
    except Exception as e:
        print(e)
    if (len(stock_list) == 0) :
        stock_list = {}
    return render_template('search.html',q=q,stock_list = stock_list,page_info = page_info)

@app.route('/get_stocks')
def get_stocks():
    stock_model = stock()
    stock_model.download_stocks()
    return 'download stocks success!'



@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001,debug=True)