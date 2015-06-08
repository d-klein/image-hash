import numpy as np

def blocks(arr, x_dim, y_dim):
    temp = np.array_split(arr,x_dim)
    res = []
    for element in temp:
        res.append(np.array_split(element,y_dim,axis=1))
    return res


def fft_hash(fxy):
    # divide into blocks and compute means
    bl = blocks(fxy,40,30)
    # compute means of blocks
    ms = []
    for x in xrange(0,len(bl)):
        els = []
        for y in xrange(0,len(bl[x])):
            els.append(np.mean(bl[x][y]))
        ms.append(els)
    # compute 2-dim fft
    ffts = np.fft.fft2(ms)
    # drop lower half (redundant freq. comp)
    n = ffts.shape[0]
    if n % 2 == 0 :
        n = n/2
    else:
        n = (n-1)/2
    ffts_half = ffts[0:(n+1)]
    sorted_idx = np.ndarray.argsort(np.absolute(ffts_half.flatten()))[::-1]
    # return sorted_idx[0:80]
    return np.absolute(ffts_half.flatten())[0:64]

def compare(pos_a, pos_b):
    diff_sum = 0
    for i in xrange(0,len(pos_a)):
        best = 100000
        for j in xrange(max(i-1,0),min(i+1,len(pos_b)-1)):
            diff = abs(pos_a[i] - pos_b[j])
            if diff < best:
                best = diff
        diff_sum = diff_sum + best
    return diff_sum

def diff1(a,b):
    sum_ = 0
    for i in xrange(1,len(a)):
        diff1 = a[i] - a[i-1]
        diff2 = b[i] - b[i-1]
        sum_ = sum_ + abs(diff1-diff2)
    return sum_









