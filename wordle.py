from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd

import numpy

df = pd.read_csv('earf.csv',encoding="ISO-8859-1")

NOPROD = df[df['Final Assessment Code']=='NOPROBDET']
#
# NOPROD.to_csv('NOPROD.csv')

PAIN = df[df['Final Assessment Code']=='PAIN']

# PAIN.to_csv('NOPROD.csv')

# mytextlist = []
# for comments in PAIN['Case Comments']:
#     mytextlist.append(str(comments)[:-1].split(' '))
#
# mytext = ''
# for comments in PAIN['Case Comments']:
#     mytext += str(comments)[:-1].lower()

mytextlist2 = []
for comments in NOPROD['Case Comments']:
    mytextlist2.append(str(comments)[:-1].split(' '))

mytext2 = ''
for comments in NOPROD['Case Comments']:
    mytext2 += str(comments)[:-1].lower()


def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    vocabSet = vocabSet | set(dataSet) #union of the two sets
    return vocabSet

def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
        print('*')
    sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]

# vocablist = createVocabList(mytext.split(' '))
# print(vocablist)

STOPWORDS.add('pt')
STOPWORDS.add('scene')
STOPWORDS.add('QAS')
STOPWORDS.add('involved')
STOPWORDS.add('wa')
STOPWORDS.add('vehicle')
STOPWORDS.add('pt left')
STOPWORDS.add('pt wa')
STOPWORDS.add('pt stated')
STOPWORDS.add('pt state')
STOPWORDS.add('pain to')
STOPWORDS.add('ct')
STOPWORDS.add('')
STOPWORDS.add(',')
STOPWORDS.add('states')
STOPWORDS.add('state')
STOPWORDS.add('stated')
STOPWORDS.add('to')
STOPWORDS.add('side')
STOPWORDS.add('due')
STOPWORDS.add('ha')
STOPWORDS.add('and')

for i in 'abcdefghijklmnopqrstuvwxyz':
    STOPWORDS.add(i)

print(len(STOPWORDS))

# vocablist = list(vocablist-STOPWORDS)
# for i in vocablist:
#     if len(i)<=3:
#         vocablist.remove(i)
# print(len(vocablist))

# print(vocablist)

# Freq = calcMostFreq(vocablist,mytext)
# print(Freq)

# print(STOPWORDS)
# STOPWORDS.add('pt')
# STOPWORDS.add('scene')
# STOPWORDS.add('QAS')
# STOPWORDS.add('involved')
# STOPWORDS.add('wa')
# STOPWORDS.add('vehicle')
# STOPWORDS.add('pt left')
# STOPWORDS.add('pt wa')
# STOPWORDS.add('pt stated')
# STOPWORDS.add('pt state')
# STOPWORDS.add('pain to')
# print(STOPWORDS)
wordcloud = WordCloud(background_color='white',stopwords=STOPWORDS,max_words=150).generate(mytext2)
plt.imshow(wordcloud,interpolation='bilinear')

plt.axis('off')
plt.show()