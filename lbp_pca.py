import Lbp
import os
import Image
from sklearn.decomposition import PCA
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
            lbps = list(flatten(Lbp.real_hash(img)))
            # print(len(flatten(lbps)))
            train.append(lbps)
            #print(lbps)

    pca = PCA(n_components=500)
    pca.fit(train)

    return pca

