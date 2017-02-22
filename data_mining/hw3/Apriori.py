import sys
import pdb
from collections import defaultdict


class Apriori:

    def __init__(self, input_file, min_support):
        self.input_file = input_file
        self.min_support = min_support
        self.transaction_list = []
        self.items_with_support = []
        self.freq_set = defaultdict(int)
        self.large_set = {}

    def _readFile(self):
        # use generator to read input file so we can deal with bigger files
        with open(self.input_file, 'rU') as f:
            for line in f:
                # strip() stripped all the white spaces
                lines = line.strip().split(',')
                lines[0] = 'age:'+lines[0]
                lines[1] = 'workclass:'+lines[1]
                lines[2] = 'fnlwgt:'+lines[2]
                lines[3] = 'education:'+lines[3]
                lines[4] = 'ed_num:'+lines[4]
                lines[5] = 'marital-status:'+lines[5]
                lines[6] = 'occupation:'+lines[6]
                lines[7] = 'relationship:'+lines[7]
                lines[8] = 'race:'+lines[8]
                lines[9] = 'sex:'+lines[9]
                lines[10] = 'capital-gain:'+lines[10]
                lines[11] = 'capital-loss:'+lines[11]
                lines[12] = 'hrs-per-week:'+lines[12]
                lines[13] = 'native-country:'+lines[13]
                yield lines

    def _initTransactionList(self):
        # the transaction_list stores all the transactions
        # return the one_cset(C1) so we can start running the Apriori algorithm
        one_cset = set()
        for record in self._readFile():
            # append each transaction into transaction list
            transaction = frozenset(record)
            self.transaction_list.append(transaction)

            # compute the 1-itemSets
            # set is used here instead of list since duplicate values
            # are not allowed in a set
            for item in transaction:
                one_cset.add(frozenset([item]))

        return one_cset

    def _processMinSupport(self, cset):
        # calculate the support for each item in the itemset(cset)
        # only add the item to the lset if it meets the minimum support requirement
        lset = set()
        local_set = defaultdict(int)
        # C1: local_set = {'A':countA,'B':countB,...}

        # calculate the count for each item
        for item in cset:
            for transaction in self.transaction_list:
                if item.issubset(transaction):
                    # global
                    self.freq_set[item] += 1 
                    # local
                    local_set[item] += 1
        # add the item to lset if it meets the minimum support requirement
        for item, count in local_set.items():
            support = float(count) / len(self.transaction_list)
            if support >= min_support:
                lset.add(item)

        return lset

    # compute the support for each item (ex: A, {B,C})
    def _getSupport(self, item):
        # compute the support(%) of an item
        return float(self.freq_set[item]) / len(self.transaction_list)

    def _selfJoin(self, item_set, length):
        # join a set wtih itself(k-1-element itemsets) and return k-element itemsets
        results = set()
        for i in item_set:
            for j in item_set:
                union = i.union(j)
                if len(union) == length:
                    results.add(union)
        return results


    def run(self):
        # run the Apriori algorithm and return items (tuple, support)
        # Pass C through the min_support criteria to get L (function _processMinSupport)
        # Now we get L1
        one_cset = self._initTransactionList()
        current_lset = self._processMinSupport(one_cset)
        k = 2
        empty_set = set([])
        while(current_lset != empty_set):
            # storing L k-1 into the dictionary
            self.large_set[k - 1] = current_lset
            # self join to get next k-item Cset (Ck)
            next_cset = self._selfJoin(current_lset, k)
            # Pass Ck through the min support criteria to get Lk
            next_lset = self._processMinSupport(next_cset)
            # move on to the Lk
            current_lset = next_lset
            k += 1

        # largeSet is in the structure of {n: Ln set}
        # largeSet = {1:[A,B,C,D,E],2:[AB,AC,AD,BD,CE],3:[ABC,ABD,ACD]}
        # go through every item in every L set, compute their support and save it in items_with_support
        for value in self.large_set.values():
            for item in value:
                self.items_with_support.append(
                    (tuple(item), self._getSupport(item)))
        # items_with_support will look like this
        # return [(A,supportA),(B,supportB),...,(AB,supportAB),....]

    def printResults(self):
        # sort the items by their support(count) and print it out
            i = 1
            for item, support in sorted(
                self.items_with_support, key=lambda i: i[1],
                reverse=True):
                print 'Item %d: %s, Support: %.3f' % (i, str(item), support)
                i += 1

    def writeResults(self):
        # write the frequent patterns to the output.csv file
        with open('apriori_output.csv', 'w') as f:
            for item, support in sorted(
                    self.items_with_support, key=lambda i: i[1],
                    reverse=True):
                f.write('%.3f, %s\n' % (support, ','.join(item)))

if __name__ == '__main__':
    # check if there are three arguments
    if len(sys.argv) != 2:
        print 'Usage: python apriori.py <MinSupport(%)>'
        sys.exit(1)

    # get input file name and minimum support
    input_file = 'adult_data_test.csv'
    min_support = float(sys.argv[1])

    ap = Apriori(input_file, min_support)
    ap.run()
    ap.printResults()

    # comment out if you don't want the result in a .csv file
    ap.writeResults()
