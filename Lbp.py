import numpy as np
from skimage.feature import local_binary_pattern
import math
#import temp
from skimage.feature import match_template

def flattn(l):
    return [item for sublist in l for item in sublist]

def blocks(arr, x_dim, y_dim):
    temp = np.array_split(arr,x_dim)
    res = []
    for element in temp:
        res.append(np.array_split(element,y_dim,axis=1))
    return res

def real_hash(fxy):
    lbp = local_binary_pattern(fxy,3,24,method='nri_uniform')
    bls = blocks(lbp, 10, 10)
    hists = []
    for i in xrange(0,10):
        for j in xrange(0,10):
            h,be = np.histogram(bls[i][j],10)
            hists.append(h)
    return hists

def bin_hash(fxy):
    lbp = local_binary_pattern(fxy,3,24)
    bls = blocks(lbp, 10, 10)
    bins = []
    for i in xrange(0,10):
        for j in xrange(0,10):
            h,be = np.histogram(bls[i][j],10)
            m = np.mean(h)
            for val in h:
                if val >= m:
                    bins.append(1)
                else:
                    bins.append(0)
    return bins



def real_hash_w(fxy):
    lbp = local_binary_pattern(fxy,3,24)
    bls = blocks(lbp,10,10)
    hists = []
    for i in xrange(1,9):
        for j in xrange(1,9):
            h,be = np.histogram(bls[i][j],10)
            hists.append(h)
    return hists

def pca_hash(fxy,pca):
    lbp = local_binary_pattern(fxy,3,24)
    #print(len(flattn(lbp)))
    #print(np.array([flattn(lbp)]).shape)
    res = pca.transform(np.array([flattn(lbp)]))
    #print(res.shape)
    return res[0]

def compare(h1,h2):
    s = 0.
    for i in xrange(0,len(h1)):
        for j in xrange(0,len(h1[i])):
            s = s + abs(h1[i][j] - h2[i][j])
    return s

def compare_one_dim(h1,h2):
    s = 0.
    for i in xrange(0,len(h1)):
        s = s + abs(h1[i] - h2[i])
    return s

def compare_cc(h1,h2):
    #a = [item for sublist in h1 for item in sublist]
    #b = [item for sublist in h2 for item in sublist]
    #print(len(a))
    #print(len(b))
    #print(a.shape)
    return temp.zncc(h1,h2,1,1,1,1,1) 

def xcorr(h1,h2):
    #print(h1.shape)
    h1_ = flattn(h1)
    #print(h1_)
    h2_ = flattn(h2)
    val = (match_template(np.array([h1_]),np.array([h2_]))[0][0])*1000
    if val < 0 :
        return 1000 + val
    else:
        return 1000 - val

# unweighted
def chi_square(h1,h2):
    s = 0.
    for i in xrange(0,len(h1)):
        for j in xrange(0,len(h1[i])):
            d = h1[i][j] - h2[i][j]
            n = h1[i][j] + h2[i][j]
            if n == 0:
                s += d*d
            else:
                s += (d*d)/n
    return s

def compare1(h1,h2):
    s = 0.
    for i in xrange(0,len(h1)):
        for j in xrange(0,len(h1[i])):
            d = abs(h1[i][j] - h2[i][j])
            s = s + math.sqrt(d*d)
    return s
