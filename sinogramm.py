import numpy as np
import scipy

A=359  # Number of sinogram exposures

# Project the sinogram

def sinogramm(img):
    sinogram=np.array([
        np.sum(
            scipy.ndimage.interpolation.rotate(
                img,a,order=1,reshape=False,mode='constant',cval=0.0
                )
            ,axis=1
            ) for a in xrange(A)
        ])
    return sinogram
