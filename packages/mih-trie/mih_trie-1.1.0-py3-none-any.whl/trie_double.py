# encoding: utf-8

import progressbar
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

        widgets=[
                    'trie to trie: ',
                    progressbar.widgets.Bar(), ' ',
                    progressbar.widgets.Percentage(), ' ',
                    '(', progressbar.widgets.SimpleProgress(), ') ',
                    progressbar.widgets.Timer(), ' ',
                    progressbar.widgets.AdaptiveETA()
                ]

        # update in trie2
        infoes = set()
        for n in progressbar.progressbar(node.infoes, widgets=widgets):
            key       = trie1.trace(n)
            value     = node.key
            node_trie = trie2.add(key, value)
        
            infoes.add(node_trie)
        
        # delete in trie1
        trie1.delete_bynode(node)
        
        # update in trie2-heap
        node.infoes = infoes
        trie2._heap.add_bynode(node)



    def tune_top(self):

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
            # rest empty --> top <= ratio
            # put more, then tune
            self._trie_top.update(key, value)
            self.tune_top()

        else:
            self._trie_rest.update(key, value)
            self.tune_rest()



    def have_top(self, key):

        return self._trie_top.have(key)



    def have_rest(self, key):

        return self._trie_rest.have(key)



    def save(self, fn):

        # full
        with open(fn, 'wb') as f:
            pickle.dump(self.__dict__, f)

        # predict
        with open('%s.top' % fn, 'wb') as f:
            pickle.dump({
                            'ratio'    : self.ratio,
                            '_trie_top': self._trie_top
                        }, f)



    def load(self, fn, predict=False):

        if not predict:
            with open(fn, 'rb') as f:
                d = pickle.load(f)
                self.__dict__.update(d)

        else:
            with open('%s.top' % fn, 'rb') as f:
                d = pickle.load(f)
                self.__dict__.update(d)
