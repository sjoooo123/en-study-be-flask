import json
import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.category.model import Category

# 初始化日志
logger = logging.getLogger('log')


def query_categorylist(params):
    """
    查询category列表
    :param params: 很复杂的对象
    :return: category实体列表
    """
    try:
        # 根据参数构造查询语句
        sqlStr = 'SELECT * FROM category '
        conditions = dict()
        # 过滤
        filterStr = ''
        if params['filter'] is not None:
            for i, filter in enumerate(params['filter']):
                iStr = str(i)
                for key, values in json.loads(filter).items():
                    orStr = 'or ' if filterStr else ''
                    filterStr += orStr + ':key' + \
                        iStr + ' IN :values' + iStr + ' '
                    conditions.update({
                        "key" + iStr: key,
                        "values" + iStr: values
                    })

        # 关键字查询

        # 排序

        linkStr = 'where ' if len(filterStr) else ''

        # 组合sql
        sqlStr = sqlStr + linkStr + filterStr

        cursor = db.session.execute(sqlStr, conditions)

        # 查询列表
        res = cursor.fetchall()

        result = []
        if res:
            keys = cursor.keys()
            for row in res:
                result_row = dict(zip(keys, row))
                result.append(result_row)

        return {'list': result}

    except OperationalError as e:
        logger.info("query_categorylist errorMsg= {} ".format(e))
        return None
