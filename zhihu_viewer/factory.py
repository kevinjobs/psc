import sqlite3
from zhihu_viewer.bottle import Bottle
from zhihu_viewer.bottle import request
from zhihu_viewer.bottle import route
from zhihu_viewer.bottle import static_file


app = Bottle()
conn = sqlite3.connect(r"D:\Backups\HolyStreet\zhihu.db")


@app.route('/view')
def view():
    return static_file('view.html', root='./zhihu_viewer/static/')


@app.error(500)
def error500(error):
    print(error)
    return 'Internal Server Error'


@app.route('/images')
def images():
    ques_title = request.query.ques_title or None
    offset = request.query.offset or 0
    limit = request.query.limit or 20

    conn.row_factory = dict_factory
    cursor = conn.cursor()
    results = cursor.execute('SELECT * FROM images WHERE question_title = ? LIMIT ? OFFSET ?', (ques_title, limit, offset))
    
    return {
        'code': 0,
        'msg': 'success',
        'data': [result for result in results]
    }


@app.route('/questions')
def questions():
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    results = cursor.execute('SELECT * FROM images')
    ques_arr = []
    for result in results:
        if result['question_title'] not in ques_arr:
            ques_arr.append(result['question_title'])

    return {
        'code': 0,
        'msg': 'success',
        'data': ques_arr,
    }


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
