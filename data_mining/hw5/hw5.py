from sklearn.cluster import KMeans
from scipy.misc import comb
import numpy

def question1(array,init1,init2,init3):
    kmeans = KMeans(n_clusters=3, init=numpy.array([init1,init2,init3])).fit(array)
    print kmeans.labels_

def selectCloestCluster(array,init1,init2,init3):
    ret=[]
    for i in array:
        d1= numpy.linalg.norm(i-init1)
        d2= numpy.linalg.norm(i-init2)
        d3= numpy.linalg.norm(i-init3)
        d=[d1,d2,d3]
        maX=min(d)
        for idx,j in enumerate(d):
            if j==maX:
                ret.append(idx)
    return ret

# The following functions accept k as the number of common items in 10 or 7 undecided options.
def probDisAB(k):
    return comb(997,k)*comb(997-k,7-k)*comb(990,7-k)/comb(997,7)**2

def probDisAC(k):
    return comb(1000,k)*comb(1000-k,10-k)*comb(990,10-k)/comb(1000,10)**2

# the reason behind y>3+x is that only when y(common items of AC) is greater than x+3(common item of AB)
# the distance of AB is greater than AC. Similar for JaccardSimilarity.
# the following function calculate the prob of different distance implementation
def calculateSumProbEcu():
    ret=[]
    for x in range(0,8):
        for y in range(0,11):
            if y>3+x:
                ret.append(probDisAB(x)*probDisAC(y))
    return sum(ret)

def calculateSumProbJaccard():
    ret = []
    for x in range(0, 8):
        for y in range(0, 11):
            if y > 3 + x:
                ret.append(probDisAB(x) * probDisAC(y))
    return sum(ret)

if __name__ == '__main__':
    data=numpy.array([[2,10],[2,5],[8,4],[5,8],[7,5],[6,4],[1,2],[4,9]])
    print selectCloestCluster(data, [2, 10], [5, 8], [1, 2])# one step result
    question1(data,[2,10],[5,8],[1,2])# kmeans result
    print calculateSumProbEcu()
    print calculateSumProbJaccard()