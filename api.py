from flask import Flask, jsonify
from flask_cors import *

from models import stat, sys, song

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/', methods=['GET'])
def about():
    return jsonify({
        'code': 200,
        'data': sys.getAboutInfo()
    })


@app.route('/gender', methods=['GET'])
def getGender():
    return jsonify({
        'code': 200,
        'data': stat.getGenderStat()
    })


@app.route('/province', methods=['GET'])
def getProvince():
    return jsonify({
        'code': 200,
        'data': stat.getProvinceStat()
    })


@app.route('/words', methods=['GET'])
def getWords():
    return jsonify({
        'code': 200,
        'data': stat.getWordsStat()
    })


@app.route('/words/<word>', methods=['GET'])
def getSentence(word):
    return jsonify({
        'code': 200,
        'data': song.getLrcByWord(word)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
