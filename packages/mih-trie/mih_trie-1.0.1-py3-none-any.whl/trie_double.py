# encoding: utf-8

import _pickle as pickle

from trie import TrieHeap


class TrieDouble(object):


    def __init__(self, ratio=None):

        self.ratio      = ratio

        self._trie_top  = TrieHeap()
        self._trie_rest = TrieHeap()



    def trie_to_trie(self, node, trie1, trie2):
        """ Delete node of trie1, Add to trie2

        Parameters
        ----------
        node: trie.heap.node in trie1

        trie1: trie

        trie2: trie
        """

        # print('trie1:', list(self._trie_top.traverse_broad()))
        # print('trie1.heap:', self._trie_top._heap._seq)
        # print('trie2:', list(self._trie_rest.traverse_broad()))
        # print('trie2.heap:', self._trie_rest._heap._seq)
        # print('*' * 80)

        # update in trie2
        infoes = set()
        for n in node.infoes:
            key       = trie1.trace(n)
            value     = node.key
            print(key, value)
            node_trie = trie2.add(key, value)
        
            infoes.add(node_trie)

        # print('trie1:', list(self._trie_top.traverse_broad()))
        # print('trie1.heap:', self._trie_top._heap._seq)
        # print('trie2:', list(self._trie_rest.traverse_broad()))
        # print('trie2.heap:', self._trie_rest._heap._seq)
        # print('*' * 80)
        
        # delete in trie1
        trie1.delete_bynode(node)
        
        # update in trie2-heap
        node.infoes = infoes
        trie2._heap.add_bynode(node)



    def tune_top(self):

        # print('value sum:', self._trie_top._heap.value_sum)
        # print('top sum', self._trie_top.count_sum)
        # print('top min', self._trie_top.count_min)
        # print('rest sum', self._trie_rest.count_sum)
        # print('ratio current after move', (self._trie_top.count_sum-self._trie_top.count_min)/\
        #       (self._trie_top.count_sum+self._trie_rest.count_sum))

        if (self._trie_top.count_sum-self._trie_top.count_min)/\
           (self._trie_top.count_sum+self._trie_rest.count_sum) >= self.ratio:

            self.trie_to_trie(self._trie_top.node_min,
                              self._trie_top,
                              self._trie_rest)



    def tune_rest(self):

        if self._trie_top.count_sum/\
          (self._trie_top.count_sum+self._trie_rest.count_sum) < self.ratio:

            self.trie_to_trie(self._trie_rest.node_max,
                              self._trie_rest,
                              self._trie_top)



    # def add(self, key, value=1):

    #     pass



    def update(self, key, value=1):

        if self._trie_top.empty:
            self._trie_top.update(key, value)

        elif self.have_top(key):
            self._trie_top.update(key, value)
            self.tune_top()

        elif self.have_rest(key):
            self._trie_rest.update(key, value)
            self.tune_rest()

        elif self._trie_rest.empty:
            self._trie_top.update(key, value)
            self.tune_top()

        else:
            self._trie_rest.update(key, value)
            self.tune_rest()



    # def delete(self, key):

    #     pass



    # def have(self, key):

    #     pass



    def have_top(self, key):

        return self._trie_top.have(key)



    def have_rest(self, key):

        return self._trie_rest.have(key)



    def save(self, fn):

        with open(fn, 'wb') as f:
            pickle.dump(self.__dict__, f)



    def load(self, fn):

        with open(fn, 'rb') as f:
            d = pickle.load(f)
            self.__dict__.update(d)
