import pymysql
import config


def getConnection():
    return pymysql.connect(host=config.DB_HOST,
                           user=config.DB_USERNAME,
                           password=config.DB_PASSWORD,
                           db=config.DB_NAME,
                           charset=config.DB_CHATSET)


def __test__():
    db = getConnection()
    cursor = db.cursor()
    sql = "SELECT * FROM %s.system" % config.DB_NAME
    cursor.execute(sql)
    res = cursor.fetchone()
    print(res)
    db.close()


if __name__ == '__main__':
    __test__()
