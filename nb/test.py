# coding: utf-8

import numpy as np
import pickle
import datetime
import sys
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from scipy import sparse

type='long'

if len(sys.argv)>1:
    type = sys.argv[1]
filename = "../data/{}/test_seg".format(type)


print '朴素贝叶斯, {} 文本:\n'.format(type)
step = 0
test_stop_at_step = 10000

Y = []
INDEX_Y = []
INDEX_X = []
VALUE   = []

read = open('./model/{}.ma.pkl'.format(type),'r')
ma = pickle.load(read)
# ma = len(sort_dic)
read.close()

with open(filename,'r') as f:
    for line in f:
        lis = line.strip('\t\n').split('\t')
        con,label = lis[0],lis[1]
        tmp = con.split(' ')
        index_x = map(lambda line: int(line.split(',')[0]), tmp)
        m = max(index_x)
        if ma < m:
            ma = m
        value = map(lambda line: int(line.split(',')[1]), tmp)
        index_y = [step for i in range(len(index_x))]
        if step == 0:
            INDEX_Y = index_y
            INDEX_X = index_x
            VALUE = value
        else:
            INDEX_Y.extend(index_y)
            INDEX_X.extend(index_x)
            VALUE.extend(value)
        Y.append(int(label))
        if step % 500==0 :
            t = str(datetime.datetime.now().isoformat())
            print '第',step,'个文档\t',t
            sys.stdout.flush()
        if step == test_stop_at_step:
            break
        step += 1
X = sparse.coo_matrix((VALUE,(INDEX_Y, INDEX_X)),shape=(len(Y),ma+1))
#X = X.todense()

clf = joblib.load('./model/{}.nb.model'.format(type))
print '\nACC:',clf.score(X,Y),'\n'