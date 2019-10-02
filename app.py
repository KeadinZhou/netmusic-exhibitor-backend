from flask import Flask, jsonify
from flask_cors import *

import DBUtil
import config

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/gender', methods=['GET'])
def getGender():
    db = DBUtil.getConnection()
    cursor = db.cursor()
    sql = "SELECT gender, cnt FROM gender_rank"
    cursor.execute(sql)
    res = cursor.fetchall()
    json = {'code': 200, 'data': []}
    for item in res:
        if int(item[0]) == 1:
            name = '男'
        elif int(item[0]) == 2:
            name = '女'
        else:
            name = '保密'
        json['data'].append({'gender': name, 'cnt': int(item[1])})
    return jsonify(json)


@app.route('/province', methods=['GET'])
def getProvince():
    db = DBUtil.getConnection()
    cursor = db.cursor()
    sql = 'SELECT province_name, cnt FROM province_rank'
    cursor.execute(sql)
    res = cursor.fetchall()
    json = {'code': 200, 'data': []}
    for item in res:
        json['data'].append({'province': str(item[0]), 'cnt': int(item[1])})
    return jsonify(json)


@app.route('/words', methods=['GET'])
def getWords():
    db = DBUtil.getConnection()
    cursor = db.cursor()
    sql = 'SELECT word, cnt_sum FROM words_rank LIMIT 100'
    cursor.execute(sql)
    res = cursor.fetchall()
    json = {'code': 200, 'data': []}
    for item in res:
        json['data'].append({'word': str(item[0]), 'cnt': int(item[1])})
    return jsonify(json)


@app.route('/words/<word>', methods=['GET'])
def getSentence(word):
    db = DBUtil.getConnection()
    cursor = db.cursor()
    GET_LIST_SQL = "SELECT song_id FROM res_word WHERE word=%s ORDER BY RAND() LIMIT 5"
    GET_NAME_SQL = "SELECT song_name FROM song WHERE song_id=%s"
    GET_SINGER_SQL = "SELECT singer_name FROM singer,singers_sing WHERE song_id=%s AND " \
                     "singer.singer_id=singers_sing.singer_id "
    GET_LRC_SQL = "SELECT lrc FROM res_lrc WHERE song_id=%s"
    cursor.execute(GET_LIST_SQL, word)
    res_list = cursor.fetchall()
    json = {'code': 200, 'data': []}
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

        json['data'].append(song_data)

    return jsonify(json)


@app.route('/', methods=['GET'])
def about():
    db = DBUtil.getConnection()
    cursor = db.cursor()
    sql = "SELECT * FROM %s.system" % config.DB_NAME
    cursor.execute(sql)
    res = cursor.fetchall()
    json = {'code': 200, 'data': {}}
    for item in res:
        json['data'][item[0]] = item[1]
    return jsonify(json)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
