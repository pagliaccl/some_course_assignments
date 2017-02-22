from collections import defaultdict
import pandas
import itertools


class FPgross():

    def __init__(self,D=None,threshold=1):
        if D is None:
            self._root = FPgross.Node()
            self._frequentItem = {}

        else:
            self._root=FPgross.Node()
            self._frequentItem={}
            self._headers={}
            self.buildTree(D,threshold)
            # self.buildHeaders()


    def buildHeaders(self):
        self._headers=dict((k,None) for k,v in self._frequentItem.items())




    def buildTree(self,D,threshold):
        self.frequentItemSetter(D,threshold)
        if isinstance(D, pandas.DataFrame):
            newD=D.itertuples(False)
        else:
            newD=D
        for d in newD:
            self.add(d)

    def frequentItemSetter(self,D,threshold):
        ret=defaultdict(lambda :0)
        if isinstance(D, pandas.DataFrame):
            newD=D.itertuples(False)
        else:
            newD=D
        for d in newD:
            for i in set(d):
                if str(i)!='nan' and i is not None:
                    ret[i]+=1
        ret=filter(lambda (x,y):y>=threshold,ret.items())
        self._frequentItem=dict(ret)

    def add(self,d):
        # TODO
        sortD=[i for i in set(d) if i in self._frequentItem and str(i)!='nan']
        if len(sortD)>0:
            sortD=sorted(sortD, key=lambda x: self._frequentItem[x],reverse=True)
            curNode = self._root
            for i in sortD:
                nextNode=curNode.search(i)

                if nextNode:
                    curNode._count+=1
                else:
                    nextNode=FPgross.Node()
                    nextNode._items=i
                    nextNode._count=1
                    curNode.add(nextNode)
                    self.addHeader(i,nextNode)

                curNode=nextNode

    def addHeader(self,i,incoming):
        if i in self._headers:
            curNode=self._headers[i]
            while curNode._neighbor:
                curNode=curNode._neighbor
            curNode._neighbor=incoming
        else:
            self._headers[i]=incoming

    def is_single_path(self,node):
        num_children=len(node._children)
        if num_children>1:
            return False
        elif num_children==0:
            return True
        else:
            return self.is_single_path(node._children.values()[0])

    def minePatters(self,threshold):
        # todo
        if self.is_single_path(self._root):
            return self.creatPatternList()
        else:
            return self.addSurffixToPattern(self.minSubTree(threshold))

    def creatPatternList(self):
        # todo
        patterns={}

        keys=self._frequentItem.keys()


        if self._root._items is None:
            surffix=[]
        else:
            surffix=[self._root._items]
            patterns[tuple(surffix)]=self._root._count
        for i in range(1, len(keys) + 1):
            for subset in itertools.combinations(keys, i):
                pattern = tuple(x for x in sorted(list(subset) + surffix) if x is not None)
                patterns[pattern] = min([self._frequentItem[x] for x in subset])

        return patterns




    def minSubTree(self,threshold):
        # todo
        patterns={}
        toMine=sorted(self._frequentItem.keys(), key=lambda x: self._frequentItem[x])
        for item in toMine:
            surffix=[]
            conditionalTreeData = []
            node=self._headers[item]
            while node:
                surffix.append(node)
                node=node._neighbor
            for sf in surffix:
                freq=sf._count
                path=[]
                parent=sf._parent
                while parent:
                    path.append(parent._items)
                    parent=parent._parent
                for j in range(freq):
                    conditionalTreeData.append(path)
            newTree=FPgross(conditionalTreeData,threshold)
            newTree._root._items=item
            newTree._root._count=self._frequentItem[item]
            subPatterns=newTree.minePatters(threshold)
            for pattern in subPatterns.keys():

                if pattern in patterns:
                    patterns[pattern] += subPatterns[pattern]
                else:
                    patterns[pattern] = subPatterns[pattern]

        return patterns

    def addSurffixToPattern(self,patterns):
        surffix=self._root._items
        if surffix:
            newPatterns={}
            for key in patterns.keys():
                if surffix not in key:
                    newPatterns[tuple(sorted(list(key)+[surffix]))]=patterns[key]
            return newPatterns
        else:
            return patterns

    class Node:

        def __init__(self):
            self._parent= None
            self._items = None
            self._count = 0
            self._children = {}
            self._neighbor=None

        @property
        def parent(self):
            return self._parent

        @property
        def children(self):
            return self._children

        @property
        def items(self):
            return self._items

        def add(self,child):
            if not isinstance(child, FPgross.Node):
                raise TypeError("Can only add a Node as children")
            if not child._items in self._children:
                self.children[child._items]=child
                child._parent=self

        def search(self,i):
            if i in self._children:
                return self._children[i]
            return None



