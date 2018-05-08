#coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
from http import cookiejar
import time
from dao import mydao

session = requests.session()
nowcoder_head = 'https://www.nowcoder.com'  #牛客官网
nowcoder_url = 'https://www.nowcoder.com/discuss?type=7&order='  #牛客讨论区

try:
    session.cookies.load(ignore_discard=True, ignore_expires=True)
except:
    pass

def newcoder(pageStart,pageEnd, key):
    for page in range(pageStart,pageEnd + 1):
        url = nowcoder_url + str(page)
        resp = session.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        ul = soup.find('ul', {'class': 'common-list'})
        li = ul.find_all('li')
        for i in range (0,len(li)):
            a = li[i].find_all('a')
            job_title = a[1].get_text().strip().strip('置顶').strip()
            if (key in a[1].get_text().strip().strip('置顶').strip()):
                job_url = nowcoder_head+a[1].attrs['href']
                p = li[i].find('p', {'class': 'feed-tip'})
                if ('今天' in p.get_text()):
                    pub_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime());
                else:
                    mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",p.get_text())
                    pub_date = mat.group(0)
                if (mydao.is_inserted(job_title) == False):
                    mydao.insert_inf(job_title,job_url,pub_date)

def tsinghua(pageStart,pageEnd, key):
    tsinghua_host = 'https://www.newsmth.net'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie':'',
        'Host': 'www.newsmth.net',
        'Referer': 'https://www.newsmth.net/nForum/',
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest'
    }
    for page in range(pageStart,pageEnd + 1):
        url = tsinghua_host + '/nForum/s/article?ajax&t1=' + key + '&au=&b=Career_Campus&p=' + str(page)
        resp = session.get(url, headers=headers)    #必须要加头部，否则请求不到数据
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.find('table', {'class': 'board-list tiz'})
        trs = table.find_all('tr')
        for i in range(2, len(trs)):       #前两个是广告，去掉
            tds = trs[i].find_all('td')    #获取标题
            a = tds[2].find('a')
            job_url = tsinghua_host + a.attrs['href']
            job_title = a.string
            pub_date = tds[3].string    #获取发布日期
            if (':' in pub_date):
                pub_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime());
            if (mydao.is_inserted(job_title) == False):
                mydao.insert_inf(job_title,job_url,pub_date)
        
if __name__ == '__main__':
    newcoder(1,14, '内推')
    newcoder(1,14, 'Java')
    tsinghua(1, 2,'Java')
    tsinghua(1, 2,'内推')
