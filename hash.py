#!/usr/bin/python

import argparse
import Image
import Average
import Difference
import Dct
import Fft
import Zernike
import PseudoZernike
import Radon
import Wu
import numpy
import Compare
import Lbp
import pickle
#import eigen
from skimage import exposure

## must be in main file due to oct2py bug
#from oct2py import octave
#octave.addpath('/home/gast/preprocess')
#def tt_pipeline(gray):
#    return octave.preproc2(gray,0.3,2,30,[],[],10)
######

def compute_hash(filename):        
    re = 64
    if args.r != None:
        re = args.r[0]
    rgb = Image.load(filename)
    gray = Image.rgb2gray(rgb)
    gray_pp = gray
    if(args.pp != None and args.pp[0] == 'gb'):
        gray_pp = Image.gauss_blur(gray,2)
    if(args.pp != None and args.pp[0] == 'tt'):
        gray_pp = tt_pipeline(gray)
    resized = Image.resize(gray_pp,re)
    img = Image.gray2real(resized)
    hash_result = []
    if(args.cm != None and args.cm[0] == "ham"):
        if(args.hm != None):
            if args.hm[0] == "ah":
                img = Image.resize(img,8)
                hash_result = Average.bin_hash(img)
            if args.hm[0] == "dh":
                img = Image.resize2(img,9,8)
                hash_result = Difference.bin_hash(img)
            if args.hm[0] == "dct":
                hash_result = Dct.bin_hash(img,8,8)
            if args.hm[0] == "zh":
                hash_result = Zernike.bin_hash(img,0,8)
            if args.hm[0] == "pzh":
                hash_result = PseudoZernike.bin_hash(img,0,11)
            if args.hm[0] == "rash":
                print("Radon Hash can only output reals")
            if args.hm[0] == "wu":
                input_wu = Image.resize(gray,384)
                hash_result = Wu.bin_hash(input_wu)
    else:
        if(args.hm != None):
            if args.hm[0] == "ah":
                img = Image.resize(img,8)
                hash_result = Average.real_hash(img)
            if args.hm[0] == "dh":
                img = Image.resize2(img,9,8)
                hash_result = Difference.real_hash(img)
            if args.hm[0] == "dct":
                #img1 = exposure.equalize_hist(img)
                hash_result = Dct.real_hash(img,8,8)
            if args.hm[0] == "zh":
                hash_result = Zernike.real_hash(img,0,12)
            if args.hm[0] == "pzh":
                hash_result = PseudoZernike.real_hash(img,0,11)
            if args.hm[0] == "lbp":                
                hash_result = Lbp.real_hash(img)
            if args.hm[0] == "lbp1":
                # im = Image.resize2(gray,220,220)
                im = Image.resize(gray,220)
                im2 = Image.gray2real(im)
                img_blur = Image.gauss_blur(im2,2)
                hash_result = Lbp.real_hash(img_blur)
                #hash_result = Lbp.bin_hash(img_blur)
            #if args.hm[0] == "lbp_pca":
            #    pcad = pickle.load(open("lbp_pca_train.p", "rb" ))
            #    hash_result = Lbp.pca_hash(img,pcad)
                #print(len(hash_result))
            #if args.hm[0] == "eigen":
            #    model = pickle.load(open("eigen_model.p", "rb" ))
            #    hash_result = eigen.transform_eigen(img,model)
            if args.hm[0] == "fft":
                hash_result = Fft.fft_hash(img)
            if args.hm[0] == "rash":
                img = Image.resize(img,63)
                hash_result = Radon.real_hash(img)
    # default
    if hash_result == []:
        print("default")
        hash_result = Dct.real_hash(img,8,8)
    return hash_result



# always print complete array as output
numpy.set_printoptions(threshold=numpy.nan)


# to add raw formatting (\n newline) 
# to help descriptions of argparse args
class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
    # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()  
        return argparse.HelpFormatter._split_lines(self, text, width)

# Base operations:
# -ch --compare-hashes hash1 hash2
# -ci --compare-images img1 img2
# -h  --hash-image img
#  
# Parameter settings:
# -r   --resize w/h
# -t   --type hash-type
# -cm --cmp comparison-method
# 


parser = argparse.ArgumentParser(description ='',\
                                 formatter_class=SmartFormatter,usage='hash [options]')
parser.add_argument('-ch',metavar=('<hash1>','<hash2>'),nargs=2, \
                     type=str,help='compare hash of <hash1> and <hash2>')
parser.add_argument('-ci',metavar=('<img1>','<img2>'),nargs=2, \
                     type=str,help='compute hash difference of <img1> \
                      and <img2>')
parser.add_argument('-hid',nargs=1,type=str,metavar='<img>',help='read \
                      <img>, hash, and display hash')
parser.add_argument('-his',nargs=2,type=str,metavar=('<img>','<out>'), \
                      help='read <img>, hash, and store hash in <out>')
parser.add_argument('-r',nargs=1,type=int,metavar='<n>',help='resize \
                      image to size n*n before hashing (default: 64)')
parser.add_argument('-hm',nargs=1,type=str,metavar='<hash method>',help="R|specify hash method:\n"
                      "    ah   : Average Hash \n"
                      "    dh   : Difference Hash\n"
                      "    dct  : DCT-II based (default) \n"
                      "    zh   : Zernike Moments\n"
                      "    pzh  : Pseudo Zernike Moments\n"
                      "    rash : Radon Hash \n"
                      "    wu   : Hash by Wu et al. \n"
                      "For references, see README.TXT")
parser.add_argument('-cm',nargs=1,type=str,metavar='<comp. method>', \
                      help="R|specify computation method:\n"
                      "    mse  : real values, compared by Mean Squared Error (default)\n"
                      "    ham  : binary values, compared by Hamming Distance")
parser.add_argument('-pp',nargs=1,type=str,metavar='<preprocess>', \
                      help="R|apply preprocessor:\n"
                      "    gb   : Gaussian Blur \n"
                      "    tt   : Preprocessing Pipeline by Triggs and Tan")

args = parser.parse_args()

# compute hash difference of two stored hashes
if args.ch != None:
    file1 = args.ch[0]
    file2 = args.ch[1]
    h1 = numpy.load(file1)
    h2 = numpy.load(file2)
    if h1[0] == 0 or h1[0] == 1:
        print(str(Compare.hamming(h1,h2)))
    else:
        print(str(Compare.mse(h1,h2)))


# compute hash and display or store in file
if args.hid != None or args.his != None:
    fn = ""
    out = ""
    if args.hid != None:
        fn = args.hid[0]
    if args.his != None:
        fn = args.his[0]
        out = args.his[1]
    hash_result = compute_hash(fn)
    if args.hid != None:
        print(str(hash_result))
    if args.his != None:
        numpy.save(out, hash_result)
        print("saved hash as: " + str(out) + ".npy")

# compute hash difference of img1 and img2
# and output to screen
if args.ci != None:
    fn1 = args.ci[0]
    fn2 = args.ci[1]
    h1 = compute_hash(fn1)
    h2 = compute_hash(fn2)
    if h1[0] == 0 or h1[0] == 1:
        print(str(Compare.hamming(h1,h2)))
    else:
        print(str(Compare.mse(h1,h2)))


