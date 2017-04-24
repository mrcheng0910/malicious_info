# encoding: utf-8
"""

注意：保证手机号为11位，否则手机各个位置的数字频率会出错。
"""

import math
import pickle

accepted_chars = '0123456789'

pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])
loc_pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])


def normalize(line):
    """标准化"""
    return [c for c in line if c in accepted_chars]


def ngram(n, l):
    """ Return all n grams from l after normalizing """
    filtered = normalize(l)
    for start in range(0, len(filtered) - n + 1):
        yield ''.join(filtered[start:start + n])


def train():
    """ 
    Write a simple model as a pickle file 
    """
    k = len(accepted_chars)
    counts = [[0 for i in xrange(k)] for i in xrange(k)]   # 转移矩阵
    loc_counts = [[0 for i in xrange(k)] for i in range(11)]  # 电话各个位置出现数字的次数

    for line in open('good_numbers.txt'):
        line = line.strip()

        # 数字出现在电话各个位置上的频率
        for cid, c in enumerate(line):
            loc_counts[cid][loc_pos[c]] += 1

        # 转移矩阵
        for a, b in ngram(2, line):
            counts[pos[a]][pos[b]] += 1


    # 位置的频率转换为log概率
    for i, row in enumerate(loc_counts):
        t = float(sum(row))
        for j in xrange(10):
            try:
                row[j] = math.log(row[j] / t)
            except ValueError:
                row[j] = 0.0

    # 转移矩阵的频率转换为log概率
    for i, row in enumerate(counts):
        s = float(sum(row))
        for j in xrange(len(row)):
            try:
                row[j] = math.log(row[j] / s)
            except ValueError:
                row[j] = 0.0

    pickle.dump({'counts': counts,'loc_counts': loc_counts}, open('detect_model.pki', 'wb'))


def avg_transition_prob(l, log_prob_mat):
    """ Return the average transition prob from l through log_prob_mat. """
    log_prob = 0.0
    transition_ct = 0
    for a, b in ngram(2, l):
        log_prob += log_prob_mat[pos[a]][pos[b]]
        transition_ct += 1
    # The exponentiation translates from log probs to probs.
    return math.exp(log_prob / (transition_ct or 1))


if __name__ == '__main__':
    train()