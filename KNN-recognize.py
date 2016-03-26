# __author__ = 'guchaojie'
# -*- coding: utf-8 -*-
import operator
from numpy import *


def handwritingClassTest():
    hwLabels = []
    # trainingFileList = os.listdir('trainingdigit/trainingset')
    trainingFileList = listdirinmac('trainingdigit/trainingset')
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        fnameStr = trainingFileList[i]
        classStr = fnameStr.split("_")[0]
        hwLabels.append(classStr)
        trainingMat[i, :] = img2vector('trainingdigit/trainingset/%s' % fnameStr)
    # testFileList = os.listdir('trainingdigit/testdigits')
    testFileList = listdirinmac('trainingdigit/testdigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fnameStr = testFileList[i]
        classStr = fnameStr.split('_')[0]
        vTest = img2vector('trainingdigit/testdigits/%s' % fnameStr)
        classifierResult = classify0(vTest, trainingMat, hwLabels, 3)
        print "classifier result: %s, the real answer:%s" % (classifierResult, classStr),
        if (classifierResult != classStr):
            errorCount += 1.0
            print "wrong"
        else:
            print "correct"
    print "error number: %d" % errorCount
    print "error rate: %f" % (errorCount / float(mTest))


# kNN algorithm
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]  # changed
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def img2vector(fname):
    f = open(fname)
    returnVec = zeros((1, 1024))
    for i in range(28):
        lineStr = f.readline()
        if lineStr[-1] == '\n':
            lineStr = lineStr[:-1]
        rownum = len(lineStr)
        for j in range(rownum):
            returnVec[0, rownum * i + j] = int(lineStr[j])
    return returnVec


def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())  # get the number of lines in the file
    returnMat = zeros((numberOfLines, 3))  # prepare matrix to return
    classLabelVector = []  # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()  # replace all '\0'(enter key)
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(listFromLine[-1].encode('hex'))  # -1 represents for the last line of the list
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))  # element wise divide
    return normDataSet, ranges, minVals

# Foe the .DS_Store in the OS X
def listdirinmac(path):
    os_list = os.listdir(path)
    for item in os_list:
        if item.startswith('.') and os.path.isfile(os.path.join(path, item)):
            os_list.remove(item)
    return os_list


handwritingClassTest()
