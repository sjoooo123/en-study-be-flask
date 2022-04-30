# 创建应用实例
import sys
from gevent import pywsgi

from wxcloudrun import app
# 启动Flask Web服务

if __name__ == '__main__':
    # 开发
    # app.run(host=sys.argv[1], port=sys.argv[2])
    # app.run(host='127.0.0.1', port=5000)
    # 线上
    server = pywsgi.WSGIServer((sys.argv[1], int(sys.argv[2])), app)
    server.serve_forever()
