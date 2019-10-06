import random

from util import DBUtil
from functools import cmp_to_key

db, cursor = DBUtil.connect()
GET_WORD_VALUE_SQL = "SELECT word,value from res_word_value"

cursor.execute(GET_WORD_VALUE_SQL)
res = cursor.fetchall()

values = {}
for item in res:
    values[item[0]] = int(item[1])


def cmpSortByValue(x, y):
    vx = values.get(x, 0)
    vy = values.get(y, 0)
    if vx == vy:
        return 0
    if vx > vy:
        return -1
    return 1


def calc(words):
    words.sort(key=cmp_to_key(cmpSortByValue))
    cnt = 0
    value_sum = 0
    used_words = []
    for word in words:
        cnt += 1
        if cnt > 10:
            break
        value = values.get(word, 0)
        value_sum += value
        if value > 0:
            used_words.append({
                'word': word,
                'value': value
            })
        random.shuffle(used_words)
    return (value_sum // max(cnt, 1)), used_words


if __name__ == '__main__':
    testSent = \
        '''
万水千山
斜阳
双手
流传
往日
眷恋
瞬间
鲜花
缠绕
白鹭
已成
容颜
浅握
相守
弄
幸福
悲欢
轻梳
江上
两侧
委婉
永远
灯如花
此刻
州
未语
羞
雨过
静夜
发丝
染
先
双眸
身边
几度
如歌般
远帆
心事
摇曳
满天
飞红
幽草
回望
倾国倾城
铜雀楼
不变
留恋
'''
    testWords = testSent.strip().split()
    print(testWords)
    print('Forecast Comments = ' + str(calc(testWords)))
