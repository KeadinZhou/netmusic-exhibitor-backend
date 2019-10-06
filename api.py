from flask import Flask, jsonify, request
from flask_cors import *

from models import stat, sys, song, forecast
from work import divRun

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/', methods=['GET'])
def api_about():
    return jsonify({
        'code': 200,
        'data': sys.getAboutInfo()
    })


@app.route('/gender', methods=['GET'])
def api_gender():
    return jsonify({
        'code': 200,
        'data': stat.getGenderStat()
    })


@app.route('/province', methods=['GET'])
def api_province():
    return jsonify({
        'code': 200,
        'data': stat.getProvinceStat()
    })


@app.route('/ages', methods=['GET'])
def api_ages():
    return jsonify({
        'code': 200,
        'data': stat.getAgesStat()
    })


@app.route('/constellation', methods=['GET'])
def api_constellation():
    return jsonify({
        'code': 200,
        'data': stat.getConstellationStat()
    })


@app.route('/publish', methods=['GET'])
def api_publish():
    return jsonify({
        'code': 200,
        'data': stat.getPublishStat()
    })


@app.route('/words', methods=['GET'])
def api_words():
    return jsonify({
        'code': 200,
        'data': stat.getWordsStat()
    })


@app.route('/words/<word>', methods=['GET'])
def api_sentence(word):
    return jsonify({
        'code': 200,
        'data': song.getLrcByWord(word)
    })


@app.route('/singer', methods=['GET'])
def api_singer():
    return jsonify({
        'code': 200,
        'data': song.getSingerRank()
    })


@app.route('/forecast', methods=['POST'])
def api_forecast():
    json_data = request.get_json()
    if 'words' in json_data:
        words = json_data['words']
    elif 'lrc' in json_data:
        words = divRun.work(json_data['lrc'])
    else:
        return jsonify({
            'code': 400
        })
    value, used_words = forecast.calc(words)
    return jsonify({
        'code': 200,
        'value': value,
        'words': used_words
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
