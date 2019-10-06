from util import DBUtil
import json


info_words = ["作曲", "作词", "演唱", "原唱", "混音", "声祭", "后期", "母带", "编曲", "监制", "特别出演", "戏装造型", "企划", "承制", "制作人", "配唱制作"]


def main():
    GET_SQL = "SELECT song_id,song_lrc FROM song"
    PUT_SQL = "INSERT INTO res_lrc(song_id,lrc) VALUES(%s,%s)"

    db = DBUtil.getConnection()
    cursor = db.cursor()

    cursor.execute(GET_SQL)
    res = cursor.fetchall()
    for item in res:
        lrc_json = json.loads(item[1])
        try:
            lrc = lrc_json['lrc']['lyric'].strip().split('\n')
            tlrc = lrc_json['tlyric']['lyric']
        except KeyError:
            continue
        if tlrc:
            continue
        words = ''
        for line in lrc:
            line = line[line.find(']')+1:].strip()
            line = line[line.find('】')+1:].strip()
            if "：" in line or ":" in line:
                continue
            words += line + " "
        words = words.strip()
        if words:
            cursor.execute(PUT_SQL, (item[0], words))
            db.commit()
            print(item[0], words)
    db.close()


if __name__ == '__main__':
    main()
