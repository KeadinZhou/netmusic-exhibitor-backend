from util import DBUtil


def getWordsStat():
    SQL = "SELECT word, cnt_sum FROM words_rank LIMIT 100"
    db, cursor = DBUtil.connect()
    cursor.execute(SQL)
    res = cursor.fetchall()
    data = list()
    for item in res:
        data.append({'word': str(item[0]), 'cnt': int(item[1])})
    return data


def getGenderStat():
    SQL = "SELECT gender, cnt FROM gender_rank"
    db, cursor = DBUtil.connect()
    cursor.execute(SQL)
    res = cursor.fetchall()
    data = list()
    gender = {1: '男', 2: '女', 0: '保密'}
    for item in res:
        data.append({'gender': gender[item[0]], 'cnt': int(item[1])})
    return data


def getProvinceStat():
    SQL = "SELECT province_name, cnt FROM province_rank"
    db, cursor = DBUtil.connect()
    cursor.execute(SQL)
    res = cursor.fetchall()
    data = list()
    for item in res:
        data.append({'province': str(item[0]), 'cnt': int(item[1])})
    return data


if __name__ == '__main__':
    print(getGenderStat())
