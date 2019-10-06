from util import DBUtil, SYSUtil
from functools import cmp_to_key


db, cursor = DBUtil.connect()

GET_WORD_RANK_SQL = "SELECT word FROM words_rank ORDER BY cnt_sum DESC"
GET_SONG_LIST_SQL = "SELECT DISTINCT song_id FROM res_word"
GET_WORDS_BY_SONG_ID_SQL = "SELECT id, song_id,word,cnt FROM res_word WHERE song_id = %s"
GET_COMMENT_CNT_BY_SONG_ID_SQL = "SELECT comments_cnt FROM song WHERE song_id = %s"
SAVE_VALUE_BY_ID_SQL ="UPDATE res_word SET value=%s WHERE id=%s"
GET_WORD_VALUE_BY_WORD_SQL = "SELECT cnt,value FROM res_word WHERE word = %s AND value>0"


def getWordsRank():
    cursor.execute(GET_WORD_RANK_SQL)
    res = cursor.fetchall()
    data = {}
    index = 0
    for item in res:
        index += 1
        data[str(item[0])] = index
    return data


def getSongList():
    cursor.execute(GET_SONG_LIST_SQL)
    res = cursor.fetchall()
    data = []
    for item in res:
        data.append(item[0])
    return data


def getWordsBySongId(song_id, rank):
    cursor.execute(GET_WORDS_BY_SONG_ID_SQL, song_id)
    res = cursor.fetchall()
    data = []

    for item in res:
        data.append({
            'id': item[0],
            'song_id': item[1],
            'word': item[2],
            'cnt': item[3],
            'rank': rank.get(str(item[2]), rank.__len__())
        })
    return data


def getCommentCntBySongId(song_id):
    cursor.execute(GET_COMMENT_CNT_BY_SONG_ID_SQL, song_id)
    res = cursor.fetchone()
    return res[0]


def sortCmpByCntAndRank(a, b):
    if a['cnt'] < b['cnt']:
        return 1
    if a['cnt'] > b['cnt']:
        return -1
    if a['rank'] < b['rank']:
        return -1
    return 1


def saveValueById(_id, value):
    cursor.execute(SAVE_VALUE_BY_ID_SQL, (value, _id))
    db.commit()


def calcEverySong():
    rank = getWordsRank()
    # print(rank['凉'])
    # print(rank['凉'])
    songs = getSongList()
    index = 0
    for song in songs:
        words = getWordsBySongId(song, rank)
        words.sort(key=cmp_to_key(sortCmpByCntAndRank))
        value = getCommentCntBySongId(song)
        cnt = 0
        for item in words:
            cnt += 1
            saveValueById(item['id'], value)
            if cnt >= 10:
                break
        index += 1
        SYSUtil.log(' Calc song_id=' + str(song) + ' Sum =' + str(songs.__len__()) + ' Index=' + str(index))


def getWordValueByWord(word):
    cursor.execute(GET_WORD_VALUE_BY_WORD_SQL, word)
    res = cursor.fetchall()
    data = []
    for item in res:
        for index in range(int(item[0])):
            data.append(item[1]//10)
    mx = 0
    values = []
    for value in set(data):
        cnt = data.count(value)
        if cnt == mx:
            values.append(value)
        if cnt > mx:
            values = [value]
            mx = cnt
    return sum(values)//max(values.__len__(), 1)


def calcEveryWord():
    rank = getWordsRank()
    for word in rank:
        values = getWordValueByWord(word)
        print(word + ' = ' + str(values))


def main():
    calcEverySong()
    calcEveryWord()


if __name__ == '__main__':
    main()
