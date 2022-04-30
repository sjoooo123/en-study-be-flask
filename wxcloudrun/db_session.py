from wxcloudrun import db


def fetch_to_dict(sql, params={}, fecth='all'):
    '''
    dict的方式返回数据
    :param sql: select * from xxx where name=:name
    :param params:{'name':'zhangsan'}
    :param fecth:默认返回全部数据，返回格式为[{},{}],如果fecth='one',返回单条数据，格式为dict
    :param bind:连接的数据，默认取配置的SQLALCHEMY_DATABASE_URL，
    :return:
    '''
    print(sql)
    resultProxy = db.session.execute(sql, params)
    if fecth == 'one':
        result_tuple = resultProxy.fetchone()
        if result_tuple:
            result = dict(zip(resultProxy.keys(), list(result_tuple)))
        else:
            return None
    else:
        result_tuple_list = resultProxy.fetchall()
        if result_tuple_list:
            result = []
            keys = resultProxy.keys()
            for row in result_tuple_list:
                result_row = dict(zip(keys, row))
                result.append(result_row)
        else:
            return []
    return result

# 记录条数


def get_count(sql, params={}):
    return int(fetch_to_dict(sql, params, fecth='one').get('count'))

# 分页


def fetch_to_dict_pagetion(sql, params={}, page=1, page_size=15):
    sql_count = """select count(*) as count from (%s) _count""" % sql
    total_count = get_count(sql_count, params)
    sql_page = '%s limit %s,%s' % (sql, (page - 1) * page_size, page_size)
    result = fetch_to_dict(sql_page, params, 'all')
    result_dict = {'list': result, 'total': total_count}
    return result_dict


# 执行单条语句（update,insert）
def execute(sql, params={}):
    print('sql', sql)
    db.session.execute(sql, params)
    db.session.commit()


# 执行多条语句，失败自动回滚
def execute_many(sqls):
    print(sqls)
    if not isinstance(sqls, (list, tuple)):
        raise Exception('type of the parameters must be list or tuple')
    if len(sqls) == 0:
        raise Exception("parameters's length can't be 0")
    for statement in sqls:
        if not isinstance(statement, dict):
            raise Exception("parameters erro")
    try:
        for s in sqls:
            db.session.execute(s.get('sql'), s.get('params'),
                               bind=db.get_engine(bind=s.get('bind', None)))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception("execute sql fail ,is rollback")
