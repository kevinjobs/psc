from zhihu_viewer.bottle import run
from zhihu_viewer.factory import app


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8989, debug=True, reloader=True)
