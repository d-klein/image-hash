import Lbp
import os
import Image
from sklearn.decomposition import PCA
import numpy as np
import pickle

def flatten(ls):
    return [item for sublist in ls for item in sublist]

def unflatten(ls,dimen):
    im = []
    j = 0
    outer = len(ls) / 200
    for j in xrange(0,outer):
        lsi = []
        for i in xrange(0,200):
            # print(str(j*220+i))
            lsi.append(ls[j*200+i])
        im.append(lsi)
    return im

def train_eigen():
    # train_dir = "/home/gast/ImageHashing/face_train/"
    train_dir = "/home/gast/ImageHashing/FEC/fec_images_autoadjust/"
    suffix = ".png"
    size = 200

    train = []
    for fn in sorted(os.listdir(train_dir)):
        if fn.endswith(suffix):
            rgb = Image.load(train_dir + fn)
            gray = Image.rgb2gray(rgb)
            resized = Image.resize(gray,size)
            img = Image.gray2real(resized)
            #lbps = list(flatten(Lbp.real_hash(img)))
            img_flat = list(flatten(img))
            # print(len(flatten(lbps)))
            train.append(img_flat)
            #print(lbps)

    t = np.array(train)
    #print("len of train"+str(t.shape))
    pca = PCA(n_components=100)
    pca.fit(train)

    return pca

def transform_eigen(img,model):
    #size = 200
    #rgb = Image.load(filename)
    #gray = Image.rgb2gray(rgb)
    #resized = Image.resize(gray,size)
    #img = Image.gray2real(resized)
    compressed = model.transform(list(flatten(img)))
    #print(str(compressed[0]))
    orig = model.inverse_transform(compressed)
    #print(len(orig))
    #print(img)
    #print(unflatten(list(flatten(img)),220))
    #Image.save(img,"1.png")
    #Image.save(unflatten(list(flatten(img)),200),"2.png")
    #Image.save(unflatten(orig[0],200),"3.png")
    return compressed[0]

model = train_eigen()
#transform_eigen("0020a.jpg",model)
pickle.dump(model, open("eigen_model.p","wb"))
