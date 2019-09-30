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
    json = {'code': 200, 'data': {}}
    json['data']['word'] = word
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
