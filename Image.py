import numpy as np
from scipy import misc
from scipy import ndimage

def load_and_resize(filename,size):
    rgb = load(filename)
    gray = rgb2gray(rgb)
    resized = resize(gray,size)
    return gray2real(resized)

def rgb2gray(img):
    return np.mean(img,-1)

def load(filename):
    return misc.imread(filename)

def gray2real(img):
    x = img.shape[0]
    y = img.shape[1]
    fxy = np.zeros((x,y),dtype=np.float_)
    for i in xrange(0,x):
        for j in xrange(0,y):
            fxy[i,j] = np.float_(img[i][j])
    return fxy

def gauss_blur(img,par):
    return ndimage.gaussian_filter(img,par)

def median_blur(img,par):
    return ndimage.median_filter(img,par)

def save(out,filename):
    misc.imsave(filename,out)

def resize(img,size):
    return gray2real(misc.imresize(img,(size,size)))

def resize2(img,size_x,size_y):
    return gray2real(misc.imresize(img,(size_x,size_y)))

def gray2real01(img):
    x = img.shape[0]
    y = img.shape[1]
    fxy = np.zeros((x,y),dtype=np.float_)
    for i in xrange(0,x):
        for j in xrange(0,y):
            fxy[i,j] = np.float_(img[i][j])/np.float_(255)
    return fxy
    
def real012gray(fxy):
    x = fxy.shape[0]
    y = fxy.shape[1]
    min_ = np.float(1000000.)
    max_ = np.float(-1000000.)
    for i in xrange(0,x):
        for j in xrange(0,y):
            if(fxy[i][j] > max_):
                max_ = fxy[i][j]
            if(fxy[i][j] < min_):
                min_ = fxy[i][j]
    img = np.zeros((x,y),dtype=np.float)
    val_range = abs(min_) + abs(max_)
    print(str(min_) + str(val_range))
    for i in xrange(0,x):
        for j in xrange(0,y):
            val = fxy[i][j]
            print(str(val))
            if(min_ < 0):
                val = val + abs(min_)
            if(min_ >= 0):
                val = val - min_
            print(str(val_range))
            print(str(val/val_range))
            val = np.int((val / val_range) * 255.0)
            if(val > 255):
                val = 255
            img[i][j] = val
    return img

