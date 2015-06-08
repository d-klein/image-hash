import Lbp
import os
import Image
from sklearn.decomposition import PCA
from skimage.feature import local_binary_pattern
import pickle
import numpy as np

def flatten(ls):
    return [item for sublist in ls for item in sublist]


def train_lbp():
    train_dir = "/home/gast/ImageHashing/face_train/"
    suffix = ".png"
    size = 200

    train = []
    for fn in sorted(os.listdir(train_dir)):
        if fn.endswith(suffix):
            rgb = Image.load(train_dir + fn)
            gray = Image.rgb2gray(rgb)
            resized = Image.resize(gray,size)
            img = Image.gray2real(resized)
            lbps = local_binary_pattern(img,3,24)
            #print(flatten(lbps))
            #print(len(flatten(lbps)))
            train.append(flatten(lbps))
            #print(lbps)

    pca = PCA(n_components=100)
    #print(len(train))
    #print(len(train[0]))
    train_np = np.array(train)
    #print(train_np.shape)
    pca.fit(train_np)
    return pca

dat = train_lbp()
pickle.dump(dat, open("lbp_pca_train.p","wb"))
