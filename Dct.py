from numpy import empty, mean
from scipy.fftpack import dct

#jpeg_quant = [[16,11,10,16,24,40,51,61], \
#              [12,12,14,19,26,58,60,55] \
#              [14,13,16,24,40,57,69,56] \ 
#              [14,17,22,29,51,87,80,62] \
#              [18,22,37,56,68,109,103,77]\
#              [24,35,55,64,81,104,113,92] \
#              [49,64,78,87,103,121,120,101] \
#              [72,92,95,98,112,100,103,99]]

#def quantization(fxy):
#    res = np.zeros((8,8),dtype = np.float_)
#    for x in xrange(0,8):
#        for y in xrange(0,8):
#            res[x][y] = round(fxy[x][y] / jpeq_quant[x][y])



# foward 2d dct-II of an image
# i.e. array
def dct2(y):
    M = y.shape[0]
    N = y.shape[1]
    a = empty([M,N],float)
    b = empty([M,N],float)

    for i in range(M):
        a[i,:] = dct(y[i,:],norm='ortho')
    for j in range(N):
        b[:,j] = dct(a[:,j],norm='ortho')

    return b

def real_hash(fxy,n,m):
    dcts = dct2(fxy)
    vals = []
    upto_x = min(n,fxy.shape[0])
    upto_y = min(m,fxy.shape[1])
    for x in xrange(0,upto_x):
        for y in xrange(0,upto_y):
            if(not (x==0 and y==0)):
                vals.append(dcts[x][y])
    return vals

def bin_hash(fxy,n,m):
    vals = real_hash(fxy,n,m)
    m = mean(vals)
    bins = []
    for v in vals:
        if v >= m:
            bins.append(1)
        else:
            bins.append(0)
    return bins


# inverse 2d dct-II of an image
# i.e. array
def idct2(b,c,d):
    #M = b.shape[0]
    #N = b.shape[1]
    M = c
    N = d
    a = empty([64,64],float)
    y = empty([64,64],float)

    for i in range(M):
        a[i,:] = dct(b[i,:])
    for j in range(N):
        y[:,j] = dct(a[:,j])

    return y
