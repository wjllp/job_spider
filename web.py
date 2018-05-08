#coding:utf-8
from flask import Flask, request
from dao import mydao
import datetime
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    infs = mydao.select_inf()
    item = ''
    for inf in infs:
        item = item + '<tr><td><a href="'+inf['url'] + '" target="_blanket">' + inf['title'] + "</a></td><td >" + str(inf['time']) + "</td></tr>"
    result = '<table border="1" cellpadding="3" cellspacing="0" style="width: 60%;margin:auto;text-align:center"><th>标题</th><th>发布时间</th>'+item+ "</table>"

    return result

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 2837)
