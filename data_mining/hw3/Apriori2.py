import numpy as np
import copy


class Apriori:
    @staticmethod
    def find_1_frequentSet(data,threshold):
        temp={}
        for i in data.itertuples(False):
            for j in i:
                if str(j)!='nan':
                    if str(j) in temp:
                        temp[str(j)]+=1
                    else: temp[str(j)]=1
        return filter(lambda (y,x):int(x)>threshold,temp.items())

    @staticmethod
    def hasnot_infrequent_subset(LK_1,union):
        #TODO
        for j in union:
            temp=copy.deepcopy(union)
            temp.remove(j)
            if not LK_1.__contains__(temp):
                return False
        return True


    @staticmethod
    def apriori_gen(Lk_1,k):
        # TODO
        i=0
        ret=[]
        while i< len(Lk_1):
            j=i+1
            while j< len(Lk_1):
                union=Lk_1[i]|Lk_1[j]

                if len(union)==k and Apriori.hasnot_infrequent_subset(Lk_1,union):

                    ret.append(union)
                j+=1
            i+=1
        return ret



    @staticmethod
    def build_apriori(D,min_sup):
        L={}
        L[1]=list({i[0]} for i in Apriori.find_1_frequentSet(D,min_sup))
        data=copy.deepcopy(D)
        k=2
        while L.get(k-1)!=[]:
            ck=Apriori.apriori_gen(L[k-1],k)

            count={}
            key=0
            # set cont to count the instance
            for i in ck:
                count[key]=0
                key+=1
            for d in data.itertuples(True):
                index=d[0]
                d=d[1:]
                setd=set(d)
                setd.discard(np.nan)
                key = 0
                Del=True
                for i in ck:
                    if setd.issuperset(i):
                        count[key]+=1
                        Del=False
                    key+=1
                if Del:
                    data.drop(index,inplace=True)
            retKey=filter(lambda (x,y) :y>=min_sup,count.items())
            ret=[ck[i] for i,j in retKey]
            L[k]=ret
            k+=1
        return L















