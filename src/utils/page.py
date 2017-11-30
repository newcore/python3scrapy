import math
import re


class page():
    page_size = 10 #每页显示的数据条数
    total_data_count = 0 #总数据数
    total_page = 0 #总页数
    current_page = 1 #当前页数
    page_url = 'page={page}' #页数链接
    page_item = 5 #只显示最多5个分页

    def __init__(self,total_data_count,current_page,page_size = 10,page_url = ''):
        self.total_data_count = total_data_count
        self.page_size = page_size
        self.total_page = int(math.ceil(self.total_data_count/int(self.page_size)))
        self.current_page = current_page
        if self.current_page > self.total_page :
            self.current_page = self.total_page
        #去除现有链接里面的page=1等类似参数
        match_page_url = re.match(r"(.*?([\?|&]page=\d+))",page_url)
        if match_page_url is not None :
            page_url = page_url.replace(match_page_url.group(2),'')
        if page_url.find('?') != -1 :
            self.page_url = page_url + '&' + self.page_url
        else :
            self.page_url = page_url + '?' + self.page_url

    def get_page_url(self,new_page):
        page_url = self.page_url
        page_url = page_url.replace('{page}',str(new_page))
        return page_url

    def get_first_page(self):
        if self.total_page != 1 :
            html = '<a href="'+self.get_page_url(1)+'">首页</a>'
        else :
            html = ''
        return html

    def get_prev_page(self):
        if self.current_page != 1:
            html = '<a href="'+self.get_page_url(self.current_page-1)+'">上一页</a>'
        else :
            html = ''
        return html

    def get_next_page(self):
        if self.current_page != self.total_page :
            html = '<a href="'+self.get_page_url(self.current_page+1)+'">下一页</a>'
        else:
            html = ''
        return html

    def get_last_page(self):
        if self.current_page != self.total_page :
            html = '<a href="'+self.get_page_url(self.total_page)+'">尾页</a>'
        else :
            html = ''
        return html

    def get_current_page(self):
        return '<a href="javascript:;">'+str(self.current_page)+'</a>'

    def show(self):
        if self.total_page == 1 :
            return ''
        page_html = '<div id="sopage">'
        page_html = page_html + self.get_first_page()
        page_html = page_html + self.get_prev_page()
        prev_page = int((self.page_item+1)/2) #当前页，前面的页面个数，如果是只显示5条，前面只显示2条
        if self.current_page <= ( prev_page + 1 ):
            first_item = 1 #第一个页的数
        elif self.total_page - self.current_page <= prev_page :
            first_item = self.total_page + 1 -self.page_item
        else :
            first_item = self.current_page - prev_page
        last_item = first_item + self.page_item - 1
        if last_item > self.total_page :
            last_item = self.total_page #最后一个页的数
        for i in range(first_item,last_item + 1) :
            if i == self.current_page :
                page_html = page_html + '<a class="this" href="javascript:;">'+str(i)+'</a>'
            else :
                page_html = page_html + '<a href="'+self.get_page_url(i)+'">'+str(i)+'</a>'

        page_html = page_html + self.get_next_page()
        page_html = page_html + self.get_last_page()
        page_html = page_html + '</div>'
        return page_html

