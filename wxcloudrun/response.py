import json

from flask import Response


def make_succ_empty_response():
    data = json.dumps({'code': 1, 'result': {}, 'msg': '请求成功'})
    return Response(data, mimetype='application/json')


def make_succ_response(data):
    data = json.dumps({'code': 1, 'result': data, 'msg': '请求成功'})
    return Response(data, mimetype='application/json')


def make_err_response(err_msg='服务器异常'):
    data = json.dumps({'code': -1, 'msg': err_msg})
    return Response(data, mimetype='application/json')
