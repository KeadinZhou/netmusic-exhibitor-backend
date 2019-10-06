from util import DBUtil


def getLrcByWord(word):
    GET_LIST_SQL = "SELECT song_id FROM res_word WHERE word=%s ORDER BY RAND() LIMIT 5"
    GET_NAME_SQL = "SELECT song_name FROM song WHERE song_id=%s"
    GET_SINGER_SQL = "SELECT singer_name FROM singer,singers_sing WHERE song_id=%s AND " \
                     "singer.singer_id=singers_sing.singer_id "
    GET_LRC_SQL = "SELECT lrc FROM res_lrc WHERE song_id=%s"
    db, cursor = DBUtil.connect()
    cursor.execute(GET_LIST_SQL, word)
    res_list = cursor.fetchall()

    data = list()

    for item in res_list:
        song_id = item[0]
        song_data = {'id': song_id}

        cursor.execute(GET_NAME_SQL, song_id)
        song_name = cursor.fetchone()[0]
        song_data['name'] = song_name

        cursor.execute(GET_SINGER_SQL, song_id)
        singer_name = cursor.fetchone()[0]
        song_data['singer'] = singer_name

        cursor.execute(GET_LRC_SQL, song_id)
        song_lrc = cursor.fetchone()[0]
        song_lrc = song_lrc.split()
        for lrc in song_lrc:
            if word in lrc:
                song_data['lrc'] = lrc
                break

        data.append(song_data)

    return data


def getSingerRank():
    SQL = "SELECT singer_id,singer_name,song_cnt,comment_cnt  FROM res_singer_rank ORDER BY comment_cnt DESC LIMIT 20"
    db, cursor = DBUtil.connect()
    cursor.execute(SQL)
    res = cursor.fetchall()
    data = list()
    for item in res:
        data.append({
            'singer_id': int(item[0]),
            'singer_name': item[1],
            'song_cnt': int(item[2]),
            'comment_cnt': int(item[3])
        })
    return data


if __name__ == '__main__':
    print(getSingerRank())
