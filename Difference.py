def bin_hash(fxy):
    size_x = fxy.shape[0]
    size_y = fxy.shape[1]
    bins = []
    for x in xrange(1,size_x):
        for y in xrange(0,size_y):
            if(fxy[x-1][y] < fxy[x][y]):
                bins.append(1)
            else:
                bins.append(0)
    return bins

def real_hash(fxy):
    size_x = fxy.shape[0]
    size_y = fxy.shape[1]
    reals = []
    for x in xrange(1,size_x):
        for y in xrange(0,size_y):
            reals.append(fxy[x-1][y] - fxy[x][y])
    return reals
