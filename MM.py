import codecs
import time

from log import *
from utils import *

LINE_SEPARATOR = get_line_separator()

'''
dict:words load from dict.txt, has already transformed to list which is python recognizable
'''


def MM(text, max_len=5, _dict=None, delimiter=" ", output=".\\result\\MMresult.txt"):
    time_s = time.time()
    s_2 = []  # split result
    s_1 = text  # the text to be split
    if text is None or len(text) == 0:
        return
    n = 0
    while n < len(s_1):
        matched = False  # if the word match the word stored in dictionary, it is true
        for i in range(max_len, 0, -1):
            s = text[n:n + i]  # select string from left with length i
            if s != LINE_SEPARATOR and notChinese(s):
                temp = i
                temp += 1
                # print("%s is letters or digit" % s)
                while notChinese(text[n:n + temp]):
                    temp += 1
                    # print("%s is letters or digit" % text[n:n + temp])
                s_2.append(text[
                           n:n + temp - 1])  # if string is made of all-num or all-digit ,it should be split out!(for this task only)
                print("%s is letters or digit,divided out" % text[n:n + temp - 1])
                n += (temp - 1)
                matched = True
                break
            # print("s:{},length:{}".format(s, i))
            if s in _dict:
                s_2.append(s)
                matched = True
                n = n + i
                print("s:{} found in dictionary.".format(s))
                break
        if not matched:
            s_2.append(s_1[n])  # text[n] is a single-character word,add it!
            n = n + 1
    time_e = time.time()
    with codecs.open(output, "w", encoding='utf-8') as f:
        f.write(delimiter.join('%s' % id for id in s_2))
    words_count = len(s_2)
    print("The split result has been written to {} .".format(os.path.abspath(output)))
    print("Total words: %d" % words_count)
    timea = time_e - time_s
    print("Time consume: %d m %.2f s" % (timea / 60, timea % 60))
    speed = words_count / timea
    print("Speed: %.2f words per second" % speed)
    with open(".\\result\\div_speed.txt", "a+") as f:
        f.write("File: %s, word count: %d, time consume: %.2f s, speed: %.2f words per second" % (
            os.path.abspath(output), words_count, timea, speed) + LINE_SEPARATOR)
    return words_count


def get_dict(dict_file_name):
    print('getting dict...')
    with codecs.open(os.path.join(".\\dict\\", dict_file_name), "r", encoding='gbk')as f:
        content = f.read()
    # print(content)
    _dict = content.split(LINE_SEPARATOR)
    # print(_dict)
    _dict.remove('')
    print('dict get')
    return _dict


def get_max_len(_dict):
    max_len = 0
    for word in _dict:
        if len(word) > max_len:
            max_len = len(word)
    return max_len


def main():
    import sys
    sys.stdout = Logger(".\\result\\div_log.txt")
    if not os.path.exists(".\\test_datas\\datas"):
        os.mkdir(".\\test_datas\\datas")
    if not os.path.exists(".\\result\\train"):
        os.mkdir(".\\result\\train")
    test_data_path = ".\\test_datas\\datas"
    output_path = ".\\result\\train"
    total = count_file(test_data_path)
    a_dict = get_dict("dict.txt")
    max_len = get_max_len(a_dict)  # use the longest word in dictionary as the max word length
    start = time.time()
    count = 0
    word_count = 0
    for filenames in get_file_list(test_data_path):
        count += 1
        filename = filenames.split('\\')[-1][0:-4]
        print("current file:" + filename + ".txt")
        f = codecs.open(filenames, 'r', encoding='gbk', errors='ignore')
        content = f.read()
        filter_text(content)  # filter out the non-character items
        f.close()
        word_count += MM(content, max_len=max_len, _dict=a_dict, delimiter=" ",
                         output=os.path.join(output_path, filename + '_div.txt'))
        time_current = time.time() - start
        print(
            "%d/%d files proceed, total time cost:%d m %.2f s" % (count, total, time_current / 60, time_current % 60))
    end = time.time()
    delta = end - start
    print("Total used time:%d m %.2f s" % (delta / 60, delta % 60))
    print("Total words :{}".format(word_count))
    print("Overall speed: %.2f words per second" % (word_count / delta))


if __name__ == '__main__':
    main()
