#!/usr/bin/env python3
import PIL.Image as img
import numpy as np
import sys
from kluster import Kluster
from random import randint

class ImgKluster(Kluster):
    def assign_rand_clusters(self):
        self.means = [
            np.array([randint(0,255), randint(0,255), randint(0,255)])
                for i in range(self.k)]
        print(self.means)
        self.clusters = [self.find_nearest_cluster(x) for x in self.xs]
        

def dimcolor(photoary, n):
    if not isinstance(photoary, np.ndarray):
        raise ValueError("np.array is required.")
    aryshape = photoary.shape
    pixelbytes = aryshape[-1]
    photoary = photoary.reshape(-1,pixelbytes)
    kluster = ImgKluster(n,10)
    kluster.feeddata(photoary)
    #clusters = kluster.analyse()
    for i in range(3):
        print(kluster.step(), len(set(kluster.clusters)))
    clusters = kluster.clusters
    # calculate mean color for each cluster.
    means = [np.zeros(pixelbytes) for k in range(n)]
    counters = [0] * n
    for (i,cl) in enumerate(clusters):
        pixel = photoary[i]
        means[cl] += pixel
        counters[cl] += 1
    means = [means[cl]/max(counters[cl],1) for cl in range(n)]
    print(means)
    
    for i in range(len(photoary)):
        photoary[i] = means[clusters[i]]
    
    return photoary.reshape(aryshape)

def make_dimmed(filename, n=10):
    photoary = np.array(img.open(filename))
    photoary = dimcolor(photoary,n)
    dimmed = img.fromarray(photoary)
    dimmed.show()
    #dimmed.save('foo.jpg')

make_dimmed('./mykitten.jpg')
