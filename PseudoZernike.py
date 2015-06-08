from scipy import misc
import numpy as np

def rad(n,m,rho):
    sum_ = 0.0
    upto = (n-abs(m))
    for s in xrange(0,upto+1):
        nom = misc.factorial(2*n+1-s)
        denom1 = misc.factorial((n-abs(m)) - s) * misc.factorial(s)
        denom2 = misc.factorial((n+abs(m)+1) - s)
        frac = nom / (denom1 * denom2)
        res = ((-1) ** s) * (rho ** (n-s)) * frac
        sum_ = sum_ + res
    return sum_

def vnm(n,m,rho,theta):
    r = rad(n,m,rho)
    vnm_r = r * np.cos(m*theta)
    vnm_i = r * np.sin(m*theta)
    return np.complex(vnm_r,vnm_i)

def zmoment(fxy,n,m):
    _N = fxy.shape[0]
    cnt = 0
    sum_ = np.complex(0.,0.)
    for x in xrange(0,_N):
        for y in xrange(0,_N):
            xn = 2*x - _N + 1
            yn = _N - 1 - 2 * y
            rho = np.sqrt(xn*xn + yn*yn) / _N
            if(rho <= 1.0):
                theta = np.arctan2(yn,xn)
                vc = np.conj(vnm(n,m,rho,theta)) * fxy[x][y]
                sum_ = sum_ + vc
                cnt = cnt + 1
    sum_ = sum_ * (n+1)/np.float(cnt) 
    return sum_

#
#
def real_hash(fxy,from_n,to_n):
    vals = []    
    for i in xrange(from_n,to_n+1):
        for j in xrange(-i,i+1):
            if((i-abs(j))%2 == 0):
                zm = zmoment(fxy,i,j)
                re = np.real(zm)
                im = np.imag(zm)
                val = np.sqrt(re*re + im*im)
                vals.append(val)
    return vals 

def bin_hash(fxy,from_n,to_n):
    bins = []
    vals = real_hash(fxy,from_n,to_n)
    mean = np.mean(vals)
    for v in vals:
        if v >= mean:
            bins.append(1)
        else:
            bins.append(0)
    return bins


# helper function that returns
# a list of tuples ((a,b),c)
# where c is the zernike moment a,b
def cache_moments(fxy,max_n):
    moments = []
    for n in xrange(0,max_n+1):
        for m in xrange(-n,n+1):
            if(((n-abs(m))%2)==0):
                z = zmoment(fxy,n,m)
                moments.append(((n,m),z))
    return moments

# finds the first tuple (s,t) in list
# with s == fst, and returns t
def find_in_list(ls,fst):
    return next(tpl[1] for tpl in ls if tpl[0] == fst)

# recomputes an image with the
# first max_n zernike moments 
def recompute(fxy,max_n):
    _N = fxy.shape[0]
    fxy_hat = np.zeros((_N,_N),dtype=np.float)
    cache = cache_moments(fxy,max_n)
    for x in xrange(0,_N):
        for y in xrange(0,_N):
            xn = 2*x-_N+1
            yn = _N-1 - 2*y
            rho = np.sqrt(xn*xn+yn*yn)/ _N
            if(rho <= 1.0):
                theta = np.arctan2(yn,xn)
                sum_ = np.complex(0.,0.)
                for n in xrange(0,max_n+1):
                    for m in xrange(-n,n+1):
                        if(((n-abs(m))%2)==0):
                            z = find_in_list(cache,(n,m))
                            v = vnm(n,m,rho,theta)
                            result = z*v
                            sum_ = sum_ + result
                fxy_hat[x,y] = np.real(sum_)
    return fxy_hat








