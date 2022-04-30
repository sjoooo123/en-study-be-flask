from ast import keyword
import json
import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.db_session import fetch_to_dict, fetch_to_dict_pagetion

# 初始化日志
logger = logging.getLogger('log')


def query_suffixlist(params):
    """
    查询suffix列表
    :param params: 很复杂的对象
    :return: suffix实体列表
    """
    try:
        # 根据参数构造查询语句
        sqlStr = 'SELECT * FROM suffix '
        # 过滤
        filterStr = ''
        if params['filter'] is not None:
            for i, filter in enumerate(params['filter']):
                for key, values in json.loads(filter).items():
                    orStr = 'or ' if filterStr else ''
                    if len(values) == 1:
                        filterStr += orStr + '%s=%s ' % (key, values[0])
                    else:
                        filterStr += orStr + '%s IN %s ' % (key, tuple(values))

        # 关键字查询
        keyStr = ''
        keyList = params['key']
        keyword = params['keyword']
        if keyword:
            for key in keyList:
                if len(keyStr) > 1:
                    keyStr += 'or %s like "%s" ' % (key, '%'+keyword+'%')
                else:
                    keyStr += '%s like "%s" ' % (key, '%'+keyword+'%')

        # 排序-暂未实现

        # 连接字符
        whereStr = ''
        andStr = ''
        if len(filterStr):
            whereStr = 'where '
            if len(keyStr):
                andStr = 'and '
        else:
            if len(keyStr):
                whereStr = 'where '

        # 组合sql
        sqlStr = sqlStr + whereStr + filterStr + andStr + keyStr

        return fetch_to_dict(sqlStr, {}) if params['all'] else fetch_to_dict_pagetion(sqlStr, {}, int(params['page']), int(params['size']))

    except OperationalError as e:
        logger.info("query_suffixlist errorMsg= {} ".format(e))
        return None
