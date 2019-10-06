import time
from util import DBUtil


def getWordsStat():
    SQL = "SELECT word, cnt_sum FROM words_rank ORDER BY cnt_sum DESC LIMIT 100"
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


def getAllUserBirthday():
    SQL = "SELECT birthday div 1000 FROM user WHERE birthday>0"
    db, cursor = DBUtil.connect()
    cursor.execute(SQL)
    res = cursor.fetchall()
    data = list()
    for item in res:
        data.append(time.localtime(item[0]))
    return data


def getAgesStat():
    birth = getAllUserBirthday()
    data = {}
    for item in birth:
        year = item.tm_year
        if year < 1930 & year > 2014:
            continue
        ages = year % 100 // 5 * 5
        data[ages] = data.get(ages, 0) + 1
    res_data = []
    ages = 30
    while ages != 15:
        tag = str(ages)+'后'
        if ages < 10:
            tag = '0' + tag
        res_data.append({
            'ages': tag,
            'cnt': data.get(ages, 0)
        })
        ages += 5
        ages %= 100
    return res_data


def getConstellation(m, d):
    if (m == 3 and d >= 21) or (m == 4 and d <= 19):
        return '白羊座'
    if (m == 4 and d >= 20) or (m == 5 and d <= 20):
        return '金牛座'
    if (m == 5 and d >= 21) or (m == 6 and d <= 21):
        return '双子座'
    if (m == 6 and d >= 22) or (m == 7 and d <= 22):
        return '巨蟹座'
    if (m == 7 and d >= 23) or (m == 8 and d <= 22):
        return '狮子座'
    if (m == 8 and d >= 23) or (m == 9 and d <= 22):
        return '处女座'
    if (m == 9 and d >= 23) or (m == 10 and d <= 23):
        return '天秤座'
    if (m == 10 and d >= 24) or (m == 11 and d <= 22):
        return '天蝎座'
    if (m == 11 and d >= 23) or (m == 12 and d <= 21):
        return '射手座'
    if (m == 12 and d >= 22) or (m == 1 and d <= 19):
        return '摩羯座'
    if (m == 1 and d >= 20) or (m == 2 and d <= 18):
        return '水瓶座'
    if (m == 2 and d >= 19) or (m == 3 and d <= 20):
        return '双鱼座'


def getConstellationStat():
    birth = getAllUserBirthday()
    data = {}
    for item in birth:
        month = item.tm_mon
        day = item.tm_mday
        con = getConstellation(month, day)
        data[con] = data.get(con, 0) + 1
    res_data = []
    for item in data:
        res_data.append({
            'constellation': item,
            'cnt': data[item]
        })
    return res_data


def getPublishStat():
    SQL = "SELECT year,cnt FROM res_publish_stat ORDER BY year"
    db, cursor = DBUtil.connect()
    cursor.execute(SQL)
    res = cursor.fetchall()
    data = []
    for item in res:
        if int(item[0]) <= 1970:
            continue
        data.append({
            'year': item[0],
            'cnt': item[1]
        })
    return data


if __name__ == '__main__':
    print(getPublishStat())
