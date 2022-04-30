from flask import request
from run import app
from wxcloudrun.category.dao import query_categorylist
from wxcloudrun.category.model import Category
from wxcloudrun.response import make_succ_response, make_err_response

PREFIX = "/api/category"


@app.route(PREFIX + '/list', methods=['GET'])
def category_list():
    """
    :return: category列表
    """

    # 获取请求地址参数
    params = request.args.to_dict(False)
    # 获取请求体参数
    # params = request.get_json()

    # 异常处理
    # if 'action' not in params:
    #     return make_err_response('缺少action参数')

    # 接收参数
    par = {}
    par['all'] = True if (
        'page' not in params or 'size' not in params) else False  # 是否全量查询
    par['page'] = params['page'] if 'page' in params else 0  # 页码
    par['size'] = params['size'] if 'size' in params else 20  # 每页数量
    # 排序-对象，暂支持单个字段排序，例：{name: 'DESC'}
    par['sorter'] = params['sorter'] if 'sorter' in params else None
    # 过滤-数组，例：[{type: ['prefix','suffix']},{type1: ['prefix','suffix']}]
    par['filter'] = params['filter[]'] if 'filter[]' in params else None
    # 关键字查询字段-多个字段使用逗号连接，默认查询名称
    par['key'] = params['key'] if 'key' in params else 'name'
    # 关键字查询字符串符串
    par['keyword'] = params['keyword'] if 'keyword' in params else None

    # 查询
    list = query_categorylist(par)
    return make_succ_response(list) if list is not None else make_err_response()
