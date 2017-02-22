import pandas as pd
import numpy
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import distance


# this function is a helper function of a cacaulcDis for quesiton 2.8.b
def normalize(series,norm):
    return series*norm/numpy.linalg.norm(series)


# this function is the for question 2.8 accepting a series of point, a target point
# , an output director that the result be saved at, and the type of distance that you want to calculate.
def cacaulcDis(it, tgt, dir,type):
    ret=[]
    if type =="euclidean":
        for i in it:
            ret.append(distance.euclidean(numpy.array(i[1],dtype=object),numpy.array(tgt,dtype=object)))
        f=open(dir,'w')
        for j in ret:
            f.writelines(str(j)+"\n")
        f.close()
    if type =="cosine":
        for i in it:
            ret.append(distance.cosine(numpy.array(i[1],dtype=object),numpy.array(tgt,dtype=object)))
        f=open(dir,'w')
        for j in ret:
            f.writelines(str(j)+"\n")
        f.close()

    if type =="chebyshev":
        for i in it:
            ret.append(distance.chebyshev(numpy.array(i[1],dtype=object),numpy.array(tgt,dtype=object)))
        f=open(dir,'w')
        for j in ret:
            f.writelines(str(j)+"\n")
        f.close()

    if type =="manhattan":
        for i in it:
            size=len(i[1])
            j=0
            temp=0
            while j<size:
                temp=temp+abs(tgt[j]-i[1][j])
                j=j+1

            ret.append(temp)
        f = open(dir, 'w')
        for k in ret:
            f.writelines(str(k) + "\n")
        f.close()

    if type=="sortNormEuc":
        for i in it:
            ret.append(distance.euclidean(normalize(numpy.array(i[1], dtype=object),1), normalize(numpy.array(tgt, dtype=object),1)))
        f = open(dir, 'w')
        ret=sorted(ret)
        for j in ret:
            f.writelines(str(j) + "\n")
        f.close()


# this function is for question 3.3 accepting a series of data and the binsize that the data should be smoothed with.
def question3_3(a,binsize):
    ret=[]
    i=0
    acumulator=0
    while i <len(a):
        acumulator += a[i]
        if((i+1)%binsize==0):
            ret.append(acumulator/binsize)
            ret.append(acumulator/binsize)
            ret.append(acumulator/binsize)
            acumulator=0
        i+=1
    return ret


# this function is a helper function that match a series of data to its index
def sequence_to_map(a):
    idx=0
    ret={}

    for i in a:
        ret[idx]=i
        idx+=1
    return ret


# the following functions are for question 3.13 a,b,c
# question a accept an unsorted series of data
# question b accept an unsorted series of data, a bin width that you wish the data to be classified with
# question b accept an unsorted series of data, a bin number that you wish the data the be classified with,
# that is the class number.
# They all out put the series of data after processing with respect of its original index.
def question3_13_a(a):
    ret=[]
    valueMap={} # this keeps the map of actual value and the value after transformation
    value=0 # this is gives the initial value after concept hierarchy
    for i in a:
        if i not in valueMap:
            valueMap[i]=value
            value += 1
        ret.append(valueMap.get(i))
        
    return ret


def question3_13_b(a,width):

    data = sequence_to_map(a)

    ret=[]
    value =0
    curcutoff=min(a)
    for k in range(0,len(a)):
        while data.get(k)>curcutoff:
            curcutoff+=width
            value+=1
        data[k]=value
    for i in range(0,len(a)):
        ret.append(data.get(i))
    return ret



def question3_13_c(a,binNumber):
    ret=[]
    data=sequence_to_map(a)
    counter=1
    value=0
    for i in range(len(a)):
        if counter>=len(a)/(binNumber-1):
            counter=1
            value+=1

        else:
            counter+=1
        data[i]=value
    for i in range(len(a)):
        ret.append(data[i])
    return ret


# The main function that out put and display results.
if __name__ == '__main__':
    # question 2.8
    data = pd.read_csv("./2_8data")
    target = (1.4, 1.6)
    cacaulcDis(data.iterrows(),target,"./chebyshev.txt",type="chebyshev")
    cacaulcDis(data.iterrows(),target,"./euclidean.txt",type="euclidean")
    cacaulcDis(data.iterrows(),target,"./manhattan.txt",type="manhattan")
    cacaulcDis(data.iterrows(),target,"./cosine.txt",type="cosine")
    cacaulcDis(data.iterrows(),target,"./sortNormEuc.txt",type="sortNormEuc")

    # question 3.3

    matplotlib.style.use('ggplot')
    data = pd.read_csv("./3_3data",header=None)
    ts = question3_3(data.iloc[0,:],3)
    pd.Series(ts).plot()
    data.iloc[0,:].plot.line()
    plt.savefig('./fig3.3.png')

    # question 3.11
    plt.close()
    data.iloc[0,:].hist(bins=6, range=(10,70))
    plt.savefig('./fig3.11_hist.png')


    # Question 3.13
    print "========The following are the test results for 3.13========"
    # A Testing with the data from 2.8
    print question3_13_a(data.iloc[0,:])
    # B Testing with the data from 2.8 with bin size 3
    print question3_13_b(data.iloc[0, :], 3)
    # C Testing with the data from 2.8 using bin number 5 and its corresponding frequency
    print question3_13_c(data.iloc[0, :],5)