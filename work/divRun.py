import jieba
import re

from util import DBUtil, SYSUtil

db = DBUtil.getConnection()
cursor = db.cursor()
stop_file = open('static/stop-words.txt')  # '../static/' if run as __main__
stop_words = stop_file.read().strip().split()
stop_file.close()

GET_SQL = "SELECT song_id,lrc FROM res_lrc"
PUT_SQL = "INSERT INTO res_word(song_id, word, cnt) VALUES(%s, %s, %s)"


def checkChinese(word):
    return re.match('[\u4E00-\u9FA5\uF900-\uFA2D]', word)


def work(lrc):
    cut_res = jieba.cut(lrc)
    res_list = []
    for item in cut_res:
        item = item.strip()
        if item in stop_words or not item or not checkChinese(item):
            continue
        res_list.append(item)
    return res_list


def count(words):
    dic = {}
    for item in set(words):
        dic[item] = words.count(item)
    return dic


def save(song_id, dic):
    for word in dic:
        cursor.execute(PUT_SQL, (song_id, word, dic[word]))
        db.commit()


def main():
    cursor.execute(GET_SQL)
    res = cursor.fetchall()
    cnt = 0
    for item in res:
        cnt += 1
        SYSUtil.log("song_id=" + str(item[0]) + " cnt=" + str(cnt))
        words = work(item[1])
        dic = count(words)
        save(item[0], dic)


def testChinese():
    SQL = "SELECT word FROM words_rank"
    cursor.execute(SQL)
    res = cursor.fetchall()
    for item in res:
        testRes = checkChinese(item[0])
        if not testRes:
            print("X", end=" ")
        else:
            print(" ", end=" ")
        print(item[0])


if __name__ == '__main__':
    main()
    # testChinese()
