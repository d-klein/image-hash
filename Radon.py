import numpy as np
from scipy.fftpack import dct

def in_gamma(x,y,xc,yc,deg):
    rad = np.pi * (deg / 180.0)
    val = (x-xc) * np.cos(rad) + (y-yc) * np.sin(rad)   
    if(val >= -0.5 and val <= 0.5):
        return True
    else:
        return False

def count_xy_in_gamma(fxy,xc,yc,deg):
    count = 0
    size_x = fxy.shape[0]
    size_y = fxy.shape[1]
    for x in xrange(0,size_x):
        for y in xrange(0,size_y):
            if(in_gamma(x,y,xc,yc,deg)):
                count = count + 1
    return count

def rash_vec(fxy):
    size_x = fxy.shape[0]
    size_y = fxy.shape[1]
    reals = []
    if(not((size_x % 2) == 1)):
        raise ValueError("Input Image for Radon Hash must haven odd size")
    xc = (size_x / 2) + 1
    yc = (size_y / 2) + 1
    for i in xrange(0,180):
        count = count_xy_in_gamma(fxy,xc,yc,i)
        sum_1 = 0.0
        sum_2 = 0.0
        for x in xrange(0,size_x):
            for y in xrange(0,size_y):
                if(in_gamma(x,y,xc,yc,i)):
                    ii = fxy[x][y]
                    sum_1 = sum_1 + (ii * ii)
                    sum_2 = sum_2 + ii
        res = (sum_1 / count) - ((sum_2/count) * (sum_2/count))
        reals.append(res)
    return reals

def real_hash(fxy):
    rv = rash_vec(fxy)
    return dct(rv)[0:40]
         
