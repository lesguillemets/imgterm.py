#!/usr/bin/env python3
from random import randint
import numpy as np
from numbers import Number

class Kluster(object):
    '''\
    class for K-mean cluster method.
    attributes:
        * Initialised in __init__:
            Kluster.k : k as in k-mean.
            Kluster.unfinished : whether repetition is not yet completed.
            Kluster.threshold : when to stop.
        * Initialised by Kluster.feeddata:
            Kluster.xs : list of data.
                -> x: number or np.array.
            Kluster.dtype : data type of data stored in Kluster.xs.
                'array' or 'number'.
            Kluster.n : == len(self.xs)
            Kluster.clusters : list of clusters each datum belongs.
                Kluster.clusters[i] corresponds to Kluster.xs[i].
                len(clusters) == Kluster.n,
                0 <= c <= k for each c in clusters.
        * Initialised in Kluster.__findmeans:
            Kluster.means : list of length Kluster.k.
                Holds the current means of the clusters.
                Each element has the same type as self.xs[0].
    '''
    
    def __init__(self,k,threshold=0):
        self.k = k
        self.unfinished = True
        self.threshold = threshold
    
    def feeddata(self, data):
        '''\
        feed list of data.
        Data should be some number, np.array or list.
        list is converted to np.array internally.
        '''
        self.n = len(data)
        if isinstance(data[0], tuple) or isinstance(data[0], list):
            self.xs = [np.array(x) for x in data]
            self.dtype = 'array'
            self._dist = self.__dist_ary
        elif isinstance(data[0], np.ndarray):
            self.dtype = 'array'
            self._dist = self.__dist_ary
            self.xs = data[:]
        elif isinstance(data[0], Number):
            self.xs = data[:]
            self.dtype = 'number'
            self._dist = self.__dist_num
        self.assign_rand_clusters()
    
    def assign_rand_clusters(self):
        if self.dtype == 'number':
            dmin, dmax = min(self.xs), max(self.xs)
            self.means = [randint(dmin,dmax) for cl in range(self.k)]
        elif self.dtype == 'array':
            dmin, dmax = np.amin(self.xs, axis=0), np.amax(self.xs, axis=0)
            #print(dmin,dmax)
            self.means = [list(map(lambda p: randint(*p), zip(dmin,dmax)))
                               for cl in range(self.k)]
        self.clusters = [self.find_nearest_cluster(x) for x in self.xs]
    
    def __findmeans(self):
        if self.dtype == 'number':
            sums = [0]*self.k
        elif self.dtype == 'array':
            sums = [np.zeros(self.xs[0].shape) for i in range( self.k)]
        counts = [0]*self.k
        for (cluster, x) in zip(self.clusters, self.xs):
            sums[cluster] += x
            counts[cluster] += 1
        self.means = [s/max(c,1) for (s,c) in zip(sums,counts)]
    
    def analyse(self):
        while True:
            changed_cluster = self.step()
            #print(changed_cluster)
            if changed_cluster <= self.threshold:
                self.__findmeans()
                break
        return self.clusters
    
    def step(self):
        self.__findmeans()
        changed_cluster = 0
        for (i,x) in enumerate(self.xs):
            nearest_cluster = self.find_nearest_cluster(x)
            if self.clusters[i] != nearest_cluster:
                changed_cluster += 1
                self.clusters[i] = nearest_cluster
        return changed_cluster
    
    def find_nearest_cluster(self,x):
        return min(
            ((self._dist(x, self.means[cl]), cl) for cl in range(self.k)))[1]
        # min( [distance_to_cluster[i], i | i <- self.k] )[1]
    
    def _dist(self, one, other):
        '''
        Kluster.feeddata defines this to be either
        Kluster.__dist_num or Kluster.__dist_ary
        in accordance with self.dtype.
        '''
        pass
    
    def __dist_num(self, one, other):
        '''
        Distance for number dtypes.
        Overwrite this method for different definitions for distance.
        '''
        return abs(one - other)
    
    def __dist_ary(self, one, other):
        '''
        Distance for arry dtypes.
        Overwrite this method for different definitions for distance.
        '''
        return sum(map(abs, one - other))


def test():
    a = Kluster(3)
    #a.feeddata([[3,4],[5,2],[43,5],[-2,53],[9,9],[0,0]])
    #a.feeddata(list(range(10)) + list(range(60,80)) + list(range(100,200)))
    a.feeddata([[randint(0,5), randint(0,5)] for i in range(10)]+
                [[randint(70,75), randint(-25,-20)] for i in range(20)] +
                [[randint(200,500),randint(-3,7)] for i in range(20)])
    print(a.dtype)
    a.analyse()
    #print(sorted(list(zip(a.clusters, a.xs)), key=lambda x:x[0]))
    result = list(zip(a.clusters, a.xs))
    result.sort(key=lambda x: x[0])
    print(list((r for r in result if r[0] == 0)))
    print(list((r for r in result if r[0] == 1)))
    print(list((r for r in result if r[0] == 2)))

if __name__ == '__main__':
    test()
