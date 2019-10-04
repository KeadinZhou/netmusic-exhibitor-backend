from util import DBUtil, config


def getAboutInfo():
    SQL = "SELECT * FROM %s.system" % config.DB_NAME
    db, cursor = DBUtil.connect()
    cursor.execute(SQL)
    res = cursor.fetchall()
    data = {}
    for item in res:
        data[item[0]] = item[1]
    return data
