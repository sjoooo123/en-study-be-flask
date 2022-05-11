from flask import request
from run import app
from wxcloudrun.common.dao import query_relatedlist
from wxcloudrun.response import make_succ_response, make_err_response

PREFIX = "/api/common"


@app.route(PREFIX + '/relatedList', methods=['GET'])
def common_related_list():
    """
    :return: 词条相关列表
    """

    # 获取请求地址参数
    params = request.args.to_dict(False)

    # 接收参数
    print(params)
    par = {}
    # 类型type="suffix"为后缀，type="prefix"为前缀，type="root"为词根
    par['type'] = params['type'][0]
    par['affix'] = params['affix'][0] if 'affix' in params else None  # 词缀
    par['wordroot'] = params['wordroot'][0] if 'wordroot' in params else None  # 词根
    par['mean'] = params['mean'][0] if 'mean' in params else None  # 英文词义
    par['translation'] = params['translation'][0] if 'translation' in params else None  # 中文词义

    # 查询
    list = query_relatedlist(par)
    return make_succ_response(list) if list is not None else make_err_response()
