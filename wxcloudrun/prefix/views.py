from flask import request
from run import app
from wxcloudrun.prefix.dao import query_prefixlist
from wxcloudrun.response import make_succ_response, make_err_response

PREFIX = "/api/prefix"


@app.route(PREFIX + '/list', methods=['GET'])
def prefix_list():
    """
    :return: prefix列表
    """

    # 获取请求地址参数
    params = request.args.to_dict(False)
    # 获取请求体参数
    # params = request.get_json()

    # 异常处理
    # if 'action' not in params:
    #     return make_err_response('缺少action参数')

    # 接收参数
    print(params)
    par = {}
    par['all'] = True if (
        'page' not in params or 'size' not in params) else False  # 是否全量查询
    par['page'] = params['page'][0] if 'page' in params else 0  # 页码
    par['size'] = params['size'][0] if 'size' in params else 20  # 每页数量
    # 排序-对象，暂支持单个字段排序，例：{name: 'DESC'}
    par['sorter'] = params['sorter'] if 'sorter' in params else None
    # 过滤-数组，例：[{type: ['prefix','suffix']},{type1: ['prefix','suffix']}]
    par['filter'] = params['filters'] if 'filters' in params else None
    # 关键字查询字段-数组表示
    par['key'] = params['key'] if 'key' in params else ['affix', 'translation']
    # 关键字查询字符串符串
    par['keyword'] = params['keyword'][0] if 'keyword' in params else None

    # 查询
    list = query_prefixlist(par)
    return make_succ_response(list) if list is not None else make_err_response()
