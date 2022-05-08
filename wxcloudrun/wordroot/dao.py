from ast import keyword
import json
import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.db_session import execute, fetch_to_dict, fetch_to_dict_pagetion

# 初始化日志
logger = logging.getLogger('log')


def query_wordrootlist(params):
    """
    查询wordroot列表
    :param params: 很复杂的对象
    :return: wordroot实体列表
    """
    try:
        # 根据参数构造查询语句
        sqlStr = 'SELECT * FROM wordroot '
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

        if len(andStr):
            keyStr = '( ' + keyStr + ') '
        # 组合sql
        sqlStr = sqlStr + whereStr + filterStr + andStr + keyStr + 'ORDER BY wordroot '

        print(sqlStr)
        return fetch_to_dict(sqlStr, {}) if params['all'] else fetch_to_dict_pagetion(sqlStr, {}, int(params['page']), int(params['size']))

    except OperationalError as e:
        logger.info("query_wordrootlist errorMsg= {} ".format(e))
        return None


def add_wordroot(params):
    """
    新增
    :param wordroot: Wordroot实体
    """
    try:
        wordroot = params['wordroot']
        translation = params['translation'] if 'translation' in params else ''
        mean = params['mean'] if 'mean' in params else ''
        example = params['example'] if 'example' in params else ''
        category = params['category'] if 'category' in params else [''],
        note = params['note'] if 'note' in params else ''

        sql = 'INSERT INTO wordroot(wordroot,translation,mean,example,category,note) VALUES("%s","%s","%s","%s","%s","%s");' % (
            wordroot, translation, mean, example, category[0], note)

        execute(sql)
    except OperationalError as e:
        logger.info("add_wordroot errorMsg= {} ".format(e))


def edit_wordroot(params):
    """
    修改
    :param wordroot: Wordroot实体
    """
    try:
        wordroot = params['wordroot']
        translation = params['translation'] if 'translation' in params else ''
        mean = params['mean'] if 'mean' in params else ''
        example = params['example'] if 'example' in params else ''
        category = params['category'] if 'category' in params else ('',),
        note = params['note'] if 'note' in params else ''
        id = params['id']

        sql = 'update wordroot set wordroot="%s",translation="%s",mean="%s",example="%s",category="%s",note="%s" where id="%s";' % (
            wordroot, translation, mean, example, category[0], note, id)
        execute(sql)
    except OperationalError as e:
        logger.info("add_wordroot errorMsg= {} ".format(e))


def delete_wordroot(params):
    """
    删除
    :param wordroot: Wordroot实体
    """
    try:
        id = params['id']

        sql = 'delete from wordroot where id="%s";' % (str(id))
        execute(sql)
    except OperationalError as e:
        logger.info("add_wordroot errorMsg= {} ".format(e))
