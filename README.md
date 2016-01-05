# Image Hashing

This repo contains various image hashing methods, implemented in python 2.
Experiments with these methods and the methods itself are described in
the paper
[A Comparative Study on Image Hashing for Document Authentication](https://github.com/d-klein/image-hash/blob/master/paper.pdf).


You can get a basic overview of usage and options with:

    hash.py --help

For example, given the supplied image sample.png, the following command creates an image hash using DCT-II and display the result to the command line:

    hash.py -hm dct -hid sample.png 

The following command saves the hash to hash_val.npy (internally using numpy.save). 

    hash.py -hm dct -his sample.png hash_val
    