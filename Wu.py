from skimage.transform import radon
import numpy as np
import itertools
import pywt
from functools import partial

def blocks(arr, x_dim, y_dim):
    temp = np.array_split(arr,x_dim)
    res = []
    for element in temp:
        res.append(np.array_split(element,y_dim,axis=1)) 
    return res

def bin_hash(fxy):
    reals = wu_hash(fxy)
    bins = []
    for ls in reals:
        m = np.mean(ls)
        for x in ls:
            if x >= m :
                bins.append(1)
            else:
                bins.append(0)
    return bins

def wu_hash(fxy):
    # compute radon hash, use 180 deg w/sampl. intervall 1
    fxy_rad = radon(fxy)
    # divide into 40x10 blocks
    bl = blocks(fxy_rad,40,10)
    # compute mean values of the blocks
    ms = []
    for x in xrange(0,len(bl)):
        els = []
        for y in xrange(0,len(bl[x])):
            els.append(np.mean(bl[x][y]))
        ms.append(els)
    # wavelet decomposition with haar wavelet
    # for each column resulting in (approx, detail)
    # approx is thrown away, resulting in a
    # list of 40 lists with each 5 higher order elements
    dec = []
    for x in xrange(0,len(ms)):
        dec.append(pywt.dwt(ms[x],"haar")[1])
    # apply fft to each component and throw imaginary
    # components away
    ffts = map(np.fft.fft,dec)
    reals = []
    for x in xrange(0,len(ffts)):
        reals_of_x = []
        for c in ffts[x]:
            reals_of_x.append(c.real)
        reals.append(reals_of_x)    
    return reals

    
