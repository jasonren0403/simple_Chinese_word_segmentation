import codecs

from log import *
from utils import *

LINE_SEPARATOR = get_line_separator()


def get_performance_score(trained_text=None, predicted_text=None, beta=1):
    '''
    准确率(Precision)和召回率(Recall)
    Precision = 正确切分出的词的数目/切分出的词的总数<本次实验只要p值，但是剩下两种评价方法的代码也写在这里了>
    Recall = 正确切分出的词的数目/应切分出的词的总数
    综合性能指标F-measure
    Fβ = (β2 + 1)*Precision*Recall/(β2*Precision + Recall)
    β为权重因子，如果将准确率和召回率同等看待，取β = 1，就得到最常用的F1-measure
    :param trained_text:
    :param predicted_text:
    :param beta:
    :return:
    '''
    # with codecs.open(".\\result\\train\\2003-4-17-99756_div.txt", 'r', 'utf-8-sig', 'ignore')as f:
    #     trained_text = f.read()
    # with codecs.open(".\\result\\example\\seg\\2003-4-17-99756_seg.txt", 'r', 'gbk', 'ignore')as f:
    #     predicted_text = f.read()
    L1 = trained_text.split(' ')
    L2 = predicted_text.split(' ')
    L1 = [x.strip() for x in L1 if x.strip() != '']
    L2 = [x.strip() for x in L2 if x.strip() != '']
    # print(len(L1), len(L2))
    print("trained(div):\n", L1)
    print("predicted(seg):\n", L2)
    total_words = len(L1)  # trained
    predicted_words = len(L2)  # predicted
    correct = 0
    gold_before = ''
    my_before = ''

    i = 1
    j = 1
    gold_before += L2[0]
    my_before += L1[0]
    if gold_before == my_before and L2[0] == L1[0]:
        correct += 1
    while i < predicted_words and j < total_words:
        changed = False
        if gold_before == my_before:
            if L2[i] == L1[j]:
                print("L2[{}]:{} matches with L1[{}]:{},correct count+1".format(i, L2[i], j, L1[j]))
                correct += 1
                gold_before += L2[i]
                my_before += L1[j]
                i += 1
                j += 1
                changed = True
            else:
                gold_before += L2[i]
                my_before += L1[j]
                i += 1
                j += 1
                changed = True
        elif len(gold_before) < len(my_before):
            gold_before += L2[i]
            i += 1
            changed = True
        elif len(gold_before) > len(my_before):
            my_before += L1[j]
            j += 1
            changed = True
        if not changed:
            try:
                raise Exception("Some problem occurs when evaluating the file.Will return.")
            except Exception as e:
                print("Problem occurs. Jumping current file")
            finally:
                return 0, 0, 0
    recall_rate = correct / total_words
    precision_rate = correct / predicted_words
    F_measure = (1 + beta) * precision_rate * recall_rate / (beta * precision_rate + recall_rate)
    print("total words: %d, predicted words: %d , correct count: %d " % (total_words, predicted_words, correct))
    print("recall rate: %.2f, precision rate: %.2f , F-measure: %.2f " % (recall_rate, precision_rate, F_measure))
    return recall_rate, precision_rate, F_measure


def main():
    import sys,os
    sys.stdout = Logger(".\\result\\evaluate_log.txt")
    data_path = ".\\result\\train"
    standard_path = ".\\result\\example\\seg"
    data_file_list = get_file_list(data_path)
    standard_file_list = get_file_list(standard_path)
    for files in data_file_list:
        file_name = files.split("\\")[-1][0:-8]
        with codecs.open(files, "r", encoding='utf-8', errors='ignore') as f:
            content_1 = f.read()
        file_2 = standard_path + "\\" + file_name + "_seg.txt"
        if file_2 in standard_file_list:
            if os.path.exists(file_2):
                with codecs.open(file_2, "r", encoding='gbk', errors='ignore') as f2:
                    content_2 = f2.read()
        print("Comparing {}.txt".format(file_name))
        recall_rate, precision_rate, F_measure = get_performance_score(content_1, content_2, 1)
        with open(".\\result\\evaluate_measurements.txt", "a+") as f:
            if recall_rate == 0 and precision_rate == 0 and F_measure == 0:
                f.write("There is some problem with the file: %s" % (os.path.abspath(files)) + LINE_SEPARATOR)
            else:
                f.write("File: %s, recall rate: %.2f, precision rate: %.2f , F-measure: %.2f " % (
                    os.path.abspath(files), recall_rate, precision_rate, F_measure) + LINE_SEPARATOR)


if __name__ == '__main__':
    main()

# if debug is needed , uncomment this and uncomment first four lines of the function below.
# Don't forget to comment if __name__ == '__main__' !(Line 101-102)
# get_performance_score()
