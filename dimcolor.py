#!/usr/bin/env python3
import PIL.Image as img
import numpy as np
import sys
from kluster import Kluster
from random import randint

def dimcolor(photoary, n):
    if not isinstance(photoary, np.ndarray):
        raise ValueError("np.array is required.")
    aryshape = photoary.shape
    pixelbytes = aryshape[-1]
    photoary = photoary.reshape(-1,pixelbytes)
    kluster = Kluster(n,10000)
    kluster.feeddata(photoary)
    clusters = kluster.analyse()
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
    import os
    photoary = np.array(img.open(filename))
    photoary = dimcolor(photoary,n)
    dimmed = img.fromarray(photoary)
    dimmed.show()
    basename, ext = os.path.splitext(filename)
    dimmed.save('{}_dim{}{}'.format(basename,n,ext))

make_dimmed('./mykitten.jpg')
