#!/usr/bin/env python3
import numpy as np
a = np.array([ [ [3,4,5], [4,5,5], [6,3,7]],
               [ [5,3,2], [2,5,2], [2,3,5]],
               [ [2,3,4], [2,3,4], [2,3,4]]])

b = np.array([  [3,4,5], [4,5,5], [6,3,7],  [5,3,2], [2,5,2], [2,3,5],  [2,3,4], [2,3,4], [2,3,4]])
k = a.shape
print(k)
b = a.reshape(1,3)
print(a)
print(b)
