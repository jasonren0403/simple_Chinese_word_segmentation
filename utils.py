import os
import platform
import re

import math


def get_line_separator():
    if platform.system() == 'Windows':
        return '\r\n'
    elif platform.system() == 'Unix':
        return '\n'
    else:
        return '\n'


def count_file(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for each in files:
            count += 1
    return count


def get_file_list(path):
    list = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            list.append(os.path.join(root, dir))
        for name in files:
            list.append(os.path.join(root, name))
    return list


def filter_text(source_text):
    text = re.sub(u"[\s+\.\!\/_,$%^*()?\[\]\"\' ]+|[<>〉《》；:\-【 】●“”+—！，\r\n。：？、~@#￥%…&*（）]+", u'', source_text)
    return text


def isEnglish(word):
    return all(97 < ord(c) < 122 or 65 < ord(c) < 90 for c in word)


def notChinese(word):
    return word.isdigit() or re.match(r"^[0-9A-Za-z]+$",word) is not None or isEnglish(word)


print(notChinese("pladaily中国"))
total_files =160
tf = 6 / total_files
idf = math.log(total_files /6)
w = tf * idf
print(w)