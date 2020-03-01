from MM import *

'''
You may run test first.
'''
LINE_SEPARATOR = get_line_separator()


def MM_test(max_len=5, _dict=None, splitator=" ", output=".\\result\\MMresult.txt"):
    with codecs.open("./test_datas/datas/[资料]十四届釜山亚运会足球比赛赛程.txt", 'r', 'gbk', 'ignore')as f:
        text = f.read()
    time_s = time.time()
    s_2 = []  # split result
    s_1 = text  # the text to split
    if text is None or len(text) == 0:
        return
    n = 0
    full_len = len(s_1)
    while n < full_len:
        matched = False  # if the word match the word stored in dictionary, it is true
        for i in range(max_len, 0, -1):
            s = text[n:n + i]  # select string from left with length i
            if s != LINE_SEPARATOR and notChinese(s):
                temp = i
                temp += 1
                print("%s is letters or digit" % s)
                while notChinese(text[n:n + temp]):
                    temp += 1
                    print("%s is letters or digit" % text[n:n + temp])
                s_2.append(text[
                           n:n + temp - 1])  # if string is made of all-num or all-digit ,it should be split out!(for this task only)
                print("%s is letters or digit,divided out" % text[n:n + temp - 1])
                n += (temp - 1)
                matched = True
                break
            print("s:{},length:{}".format(s, i))
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
        f.write(splitator.join('%s' % id for id in s_2))
    print("The split result has been written to {} .".format(os.path.abspath(output)))
    print("Total words: %d" % len(s_2))
    print("Time consume: %d m %.2f s" % ((time_e - time_s) / 60, (time_e - time_s) % 60))
    word_count = len(s_2)
    delta = time_e - time_s
    print("Speed: %.2f words per second" % (word_count / delta))
    with open(".\\result\\speed.txt", "a+") as f:
        f.write("total words: " + str(word_count) + " time: " + str(delta) + "s  speed: " + str(
            word_count / delta) + " words per second" + LINE_SEPARATOR)


def Test_MM():
    import sys
    sys.stdout = Logger(".\\result\\log.txt")
    d_dict = get_dict("dict.txt")
    MM_test(max_len=get_max_len(d_dict), _dict=d_dict)


Test_MM()

# def main():
#     recall_rate=[]
#     precision_rate=[]
#     F_measure=[]
#     line_count=0
#     with open("./result/evaluate_measurements.txt", "r") as f:
#         line_count+=1
#         lines = f.readlines()
#         lines=[x.strip() for x in lines if x!='\n']
#         for line in lines:
#             if 'There is some problem with the file' in line:
#                 continue
#             else:
#                 pattern=re.compile(r'\d+\.\d+')
#                 m=pattern.findall(line)
#                 recall_rate.append(m[0])
#                 precision_rate.append(m[1])
#                 F_measure.append(m[2])
#     print("Recall rate:",recall_rate)
#     print("Precision rate:",precision_rate)
#     print("F_measure:",F_measure)
#     recall_rate = list(map(float, recall_rate))
#     precision_rate = list(map(float,precision_rate))
#     F_measure = list(map(float,F_measure))
#     print(sum(recall_rate)/len(recall_rate))
#     print(sum(precision_rate)/len(precision_rate))
#     print(sum(F_measure)/len(F_measure))


# main()
