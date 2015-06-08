import math
import numpy

def real2bin(vals):
    m = numpy.mean(vals)
    bins = []
    for v in vals:
        if v >= m:
            bins.append(1)
        else:
            bins.append(0)
    return bins

def hamming(a,b):
    if not len(a) == len(b):
        raise ValueError('arguments not of same length')
    a_bin = real2bin(a)
    b_bin = real2bin(b)
    #print(a_bin)
    #print(b_bin)
    miss = 0
    for i in xrange(0,len(a)):
        if not a_bin[i] == b_bin[i]:
            miss = miss + 1
    return miss



#def hamming(a,b):
#    if not len(a) == len(b):
#        raise ValueError('arguments not of same length')
#    miss = 0
#    for i in xrange(0,len(a)):
#        if not a[i] == b[i]:
#            miss = miss + 1
#    return miss

def mh(a,b):
    if not len(a) == len(b):
        raise ValueError("arguments not of same length")
    diff = 0.
    for i in xrange(0,len(a)):
        d = abs(a[i] - b[i])
        diff = diff + d
    return diff

def mse(a,b):
    if not len(a) == len(b):
        raise ValueError('arguments not of same length')
    diff = 0.
    for i in xrange(0,len(a)):
        d = abs(a[i] - b[i])
        diff = diff + (d*d)
    return diff

def euc(a,b):
    if not len(a) == len(b):
        raise ValueError('arguments not of same length')
    diff = 0.
    for i in xrange(0,len(a)):
        d = a[i] - b[i]
        #print(str(d)+ " "+str(a[i]))
        diff = diff + (d*d)
    return math.sqrt(diff)

def xcorr0(a,b,delay):
    if not len(a) == len(b):
        raise ValueError('arguments not of same length')
    l = len(a)
    mu_x = float(numpy.mean(a))
    mu_y = float(numpy.mean(b))
    rd = 0.0
    nom = 0.0
    denom_x = 0.0
    denom_y = 0.0
    for i in range(0,len(a)):
        x_i = float(a[i])
        i_plus_d = (i+delay)
	y_id = 0
	if(i_plus_d < l):
            y_id = float(b[i_plus_d])
        nom += (x_i - (mu_x))*(y_id - mu_y)
        denom_x += (x_i - mu_x) * (x_i - mu_x)
        denom_y += (y_id - mu_y) * (y_id - mu_y)
    res_d = nom / (math.sqrt(denom_x) * math.sqrt(denom_y))
    return res_d

def xcorr(a,b,delay):
    if not len(a) == len(b):
        raise ValueError('arguments not of same length')
    l = len(a)
    mu_x = float(numpy.mean(a))
    mu_y = float(numpy.mean(b))
    rd = 0.0
    nom = 0.0
    denom_x = 0.0
    denom_y = 0.0
    for i in range(0,len(a)):
        x_i = float(a[i])
        i_plus_d = (i+delay) % l
        y_id = float(b[i_plus_d])
        nom += (x_i - (mu_x))*(y_id - mu_y)
        denom_x += (x_i - mu_x) * (x_i - mu_x)
        denom_y += (y_id - mu_y) * (y_id - mu_y)
    res_d = nom / (math.sqrt(denom_x) * math.sqrt(denom_y))
    return res_d

def pcc(a,b):
    if not len(a) == len(b):
        raise ValueError("arguements not of same length")
    return max([ xcorr0(a,b,delay) for delay in range(0,len(a)) ])

def cross_correlate(a,b):
    if not len(a) == len(b):
        raise ValueError('arguments not of same length')
    else:
        return numpy.correlate(a,b)
