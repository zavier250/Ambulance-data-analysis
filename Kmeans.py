import pandas as pd
import requests
import json
from numpy import *


#Get location data

def get_accident_loc(fileName,volume):
    CSV_FILE_PATH = fileName
    df = pd.read_csv(CSV_FILE_PATH, encoding="ISO-8859-1")

    df2 = pd.DataFrame(columns=('EARF Number', 'LAT', 'LON'))
    for i in range(volume):
        addr = str(df['Street Name'][i]) + ', ' + str(df['Suburb'][i])
        r = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + addr)
        if r.text == '[]':
            r = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + str(df['Street Name'][i]))
            # r=json.loads(r.text[1:-1])
        r = json.loads(r.text)
        # Data Cleaning
        if r != []:
            for detail in r:
                if -9.0 >= float(detail['lat']) >= -30.0 and 154.0 >= float(detail['lon']) >= 137.0:
                    df2 = df2.append(
                        pd.DataFrame(
                            {'EARF Number': [df['EARF Number'][i]], 'LAT': [float(detail['lat'])], 'LON': [float(detail['lon'])]}),
                        ignore_index=True)
                    print('EARF: %s, Lat: %d, Lon: %e' % (
                    df['EARF Number'][i], float(detail['lat']), float(detail['lon'])))
                    break

    # df2.to_csv('earf_loc.csv')
    print('-----Location data is successfully generated!-----')
    return df2.values

# dataMat = get_accident_loc('earf.csv')
# print(dataMat)
# CSV_FILE_PATH = './earf.csv'
# df = pd.read_csv(CSV_FILE_PATH, encoding="ISO-8859-1")
# df2=pd.DataFrame(columns=('EARF Number','LAT','LON'))
# for i in range(10):
#     addr = str(df['Street Name'][i]) + ', ' + str(df['Suburb'][i])
#     r = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + addr)
#     if r.text == '[]':
#         r = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + str(df['Street Name'][i]))
#         # r=json.loads(r.text[1:-1])
#     r=json.loads(r.text)
#     if r!=[]:
#         print(len(r))
#         for detail in r:
#             if -9.0 >= float(detail['lat']) >= -30.0 and 154.0 >= float(detail['lon']) >= 137.0:
#                 df2 = df2.append(
#                     pd.DataFrame({'EARF Number': [df['EARF Number'][i]], 'LAT': [detail['lat']], 'LON': [detail['lon']]}),
#                     ignore_index=True)
#                 break
# df2.to_csv('earf_loc.csv')

'''
前十行中发现地理位置重合的，可能为某一重大交通事件，派遣了多辆救护车
'''
#Data cleaning
'''
Check if location is in QLD
'''

#K-means
def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        print(curLine)
#         print(curLine)
        fltLine = list(map(float,curLine))
#         print(fltLine)
        dataMat.append(fltLine)
    return dataMat

# dataMat = loadDataSet('earf_loc.csv')
# print(dataMat)

def distEclud(VecA,VecB):
    return sqrt(sum(power(VecA - VecB,2)))

def distSLC(vecA,vecB):
    a = sin(vecA[0,1]*pi/180) * sin(vecB[0,1]*pi/180)
    b = cos(vecA[0,1]*pi/180) * cos(vecB[0,1]*pi/180) * \
                      cos(pi * (vecB[0,0]-vecA[0,0]) /180)
    return arccos(a + b)*6371.0



def randCent(dataSet,k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    index_list = list(range(len(dataSet)))
    random.shuffle(index_list)
    for i in range(k):
        centroids[i] = dataSet[index_list[i]]
    print('-----Centroids generated-----')
    return centroids


def kMeans(dataSet, k, distMeas=distEclud,createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataSet,k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i,0] != minIndex:
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        # print(centroids)
        for cent in range(k):
#             print(nonzero(clusterAssment[:,0]))
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            # print("ptsInClust: ")
            print(len(ptsInClust))
            centroids[cent,:] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment


def biKmeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList =[centroid0] #create a list with one centroid
    for j in range(m):#calc initial Error
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            print("sseSplit, and notSplit: ",sseSplit,sseNotSplit)
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        print('the bestCentToSplit is: ',bestCentToSplit)
        print('the len of bestClustAss is: ', len(bestClustAss))
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
    return mat(centList), clusterAssment





if __name__=='__main__':
    dataMat = get_accident_loc('earf.csv')
    dataMat = dataMat[:, 1:]
    n = shape(dataMat)
    # print(n)
    # print(dataMat)
    centroids, clusterAssment = kMeans(dataMat,2)
    # print(centroids)
    # print(clusterAssment)

