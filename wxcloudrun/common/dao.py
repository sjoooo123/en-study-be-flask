from ast import keyword
import json
import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.db_session import fetch_to_dict

# 初始化日志
logger = logging.getLogger('log')


def query_relatedlist(params):
    """
    查询词条相关列表
    :param params: 很复杂的对象
    :return: 实体列表
    """
    try:
        type = params['type']
        affix = params['affix']
        wordroot = params['wordroot']
        mean = params['mean']
        translation = params['translation']

        # 根据type查询对应的表
        sqlStr = 'SELECT * FROM %s where ' % (type)

        # 词缀
        affixStr = ''
        if affix is not None:
            affix = affix.split(',')
            for item in affix:
                orStr = 'or' if len(affixStr) else ''
                affixStr += '%s affix like "%s" ' % (orStr, item)

        # 词根
        wordrootStr = ''
        if wordroot is not None:
            wordroot = wordroot.split(',')
            for item in wordroot:
                orStr = 'or ' if len(wordrootStr) else ''
                wordrootStr += '%s wordroot like "%s" ' % (orStr, item)

        # 英文词义
        meanStr = ''
        if mean is not None:
            mean = mean.split(',')
            for item in mean:
                orStr = 'or' if len(meanStr) else ''
                meanStr += '%s mean like "%s" ' % (orStr, item)

        # 中文词义
        translationStr = ''
        if translation is not None:
            translation.replace('、', '，')
            translation.replace('；', '，')
            translation = translation.split('，')
            for item in translation:
                orStr = 'or' if len(translationStr) else ''
                translationStr += '%s translation like "%s" ' % (orStr, item)

        link1Str = 'or ' if len(affixStr) else ''
        link2Str = 'or ' if len(wordrootStr) else ''
        link3Str = 'or ' if len(meanStr) and len(translationStr) else ''

        # 排序字段
        fieldStr = 'wordroot' if type == 'wordroot' else 'affix'

        # 组合sql
        sqlStr = sqlStr + affixStr + link1Str + wordrootStr + link2Str + \
            meanStr + link3Str + translationStr + 'ORDER BY %s ' % (fieldStr)

        return fetch_to_dict(sqlStr, {})

    except OperationalError as e:
        logger.info("query_relatedlist errorMsg= {} ".format(e))
        return None
