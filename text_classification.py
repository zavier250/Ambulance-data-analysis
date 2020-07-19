import pandas as pd
from numpy import *


def loadSampleData(filename, row_num):
    df = pd.read_csv(filename, encoding="ISO-8859-1", nrows=row_num)
    comments_list = []
    classVec = []
    for i in range(row_num):
        comment_list = str(df['Case Comments'][i]).split(' ')
        comments_list.append(comment_list)
    print('-----Comments list generated-----')
    for i in range(row_num):
        label = df['Class'][i]
        classVec.append(label)
    return comments_list, classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    countClass1 = 0
    countClass2 = 0
    countClass3 = 0
    for label in trainCategory:
        if label==1:
            countClass1+=1
        elif label==2:
            countClass2+=1
        else:
            countClass3+=1
    p1 = countClass1/float(numTrainDocs)
    p2 = countClass2/float(numTrainDocs)
    p3 = countClass3/float(numTrainDocs)
    p1Num = ones(numWords)
    p2Num = ones(numWords)
    p3Num = ones(numWords)  #change to ones()
    p1Denom = 2.0
    p2Denom = 2.0
    p3Denom = 2.0   #change to 2.0
    for i in range(numTrainDocs):
        # print(trainMatrix[i])
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        elif trainCategory[i] == 2:
            p2Num += trainMatrix[i]
            p2Denom += sum(trainMatrix[i])
        elif trainCategory[i] == 3:
            p3Num += trainMatrix[i]
            p3Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)          #change to log()
    p2Vect = log(p2Num/p2Denom)          #change to log()
    p3Vect = log(p3Num/p3Denom)
    return p1Vect,p2Vect,p3Vect,p1,p2,p3

def classifyNB(vec2Classify, p1Vec, p2Vec, p3Vec, pClass1, pClass2,pClass3):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    p2 = sum(vec2Classify * p2Vec) + log(pClass2)
    p3 = sum(vec2Classify * p3Vec) + log(pClass3)
    max_value = max(p1,p2,p3)
    if max_value == p1:
        return 1
    elif max_value == p2:
        return 2
    else:
        return 3

def testingNB(filename,row_num,testEntry):
    listOPosts,listClasses = loadSampleData(filename,row_num)
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p1Vect,p2Vect,p3Vect,p1,p2,p3 = trainNB0(array(trainMat),array(listClasses))
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    return 'classified as: '+ str(classifyNB(thisDoc, p1Vect, p2Vect, p3Vect, p1, p2,p3))


# comments_list, classVec = loadSampleData('labeled.csv', 50)
# vocabList = createVocabList(comments_list)
# trainMat=[]
# for comment in comments_list:
#     trainMat.append(setOfWords2Vec(vocabList,comment))
#
# p1Vect,p2Vect,p3Vect,p1,p2,p3 = trainNB0(trainMat,classVec)
# print(p1)
# print(len(vocabList))
testDoc = 'QAS c/t 18yo F. O/a pt found sitting in drivers seat of car, fully alert, good colour. Pt states she rear-ended car in front whilst turning right at lights at <15km/h, hit R) knee on front panel, denies other injuries, denies c-spine pain, nil spontaneous neck pain. Pt was wearing seatbelt denies chest injuries or pain, nil bruising to chest. Nil airbags in car and speed low mech, minimal damagae to car --> minor crumpling of front bonnet. Nil neck pain on movement. States did not hit head, nil ALOC. Pt mobilised to stretcher, denies alcohol involvement. O/E: swelling and pain to R) knee, nil deformity, nil dislocation, good distal perfusion, reduced movement in knee but distal extremity function normal, vitals WNR. Goos dorsalis pedis and posterior tibial pulses.Pain managed with methoxyflurane and ice pack, further pain management refused (panadol and morphine/fentanyl), PMHx of R) knee reconstruction 4/12 ago due to torn ACL, tx to QEII. Delayed on scene whilst waiting for 2nd crew (501324) due to 2nd patient.'
label = testingNB('labeled.csv',50,testDoc)
print(label)
