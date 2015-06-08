# calculates various comparison stats
# for two images ets

import math
#import pylab as pl
from matplotlib import pyplot
from sklearn.metrics import auc
import os.path
import sys
import re
import commands
import subprocess
import Compare
import numpy
import Fft
import Lbp
import pca

def run_command(cmd):
    '''given shell command, returns communication tuple of stdout and stderr'''
    return subprocess.Popen(cmd, 
                            stdout=subprocess.PIPE, 
                            stdin=subprocess.PIPE).communicate()

#=======================================
# Configuration
#=======================================

enrol_dir =   "/home/gast/facealign/src/fec/enrol/dct_1212_gb/"
scan_dir  =   "/home/gast/facealign/src/fec/scan/dct_1212_gb/"

#enrol_dir =   "/home/gast/ImageHashing/feret_plus_scan/feret/lbp_220_g2/"
#scan_dir  =    "/home/gast/ImageHashing/feret_plus_scan/scan/lbp_220_g2/"
statfile = "test_stat"

TITLE = "DCT"               # title of the resulting ROC-image. This string is plotted into the image
PRECISION = 1000            # the higher the value the more steps will be made to slowly increase the threshold (recommended: 1000-5000)


#=======================================
# Operating Code
#=======================================

compare = "/home/gast/zernike/hash.py -ch "
suffix = ".npy"

enrols = []
scans = []
print("reading hashes of enrolment")
for fn_enrol in sorted(os.listdir(enrol_dir)):
    if(fn_enrol.endswith(suffix)):
        h1 = numpy.load(enrol_dir + fn_enrol)
        enrols.append((fn_enrol,h1))

print("reading hashes of scans")
for fn_scan in sorted(os.listdir(scan_dir)):
    if(fn_scan.endswith(suffix)):
        h1 = numpy.load(scan_dir + fn_scan)
        scans.append((fn_scan,h1))

#print("reading training model")
#model = pca.train_lbp()

T = 0
F = 0
MSE = []
labels = []
max_MSE = 0.0
correct_best_hits = 0
gen_best_snd = []
for (fn_enrol,h1) in enrols:
    best     = 100000000.0
    snd_best = 100000000.0
    correct =  100000000.0
    best_name = ""
    snd_best_name = ""
    correct_name = ""
    #print(str(fn_enrol))
    for (fn_scan,h2) in scans:
        no1 = re.findall(r'\d+\D',fn_enrol)[0]
        no2 = re.findall(r'\d+\D',fn_scan)[0]
        #print("no1:"+str(no1))
        #print("no2:"+str(no2))
        # print("comparing "+fn_enrol+" with "+fn_scan)
        # print("no1: "+str(no1)+" no2: "+str(no2))
        # m = Lbp.chi_square(h1,h2)
        #h1_trans = model.transform(pca.flatten(h1))
        #h2_trans = model.transform(pca.flatten(h2))
        #print("transformed models:")
        #print(h1_trans)
        #print(h2_trans)
        # m = Lbp.compare_one_dim(h1_trans[0],h2_trans[0])
        # m = Lbp.compare(h1,h2)
        #m = Compare.mh(h1,h2)
        m = 1.0 - Compare.pcc(h1,h2)
        #print(m)
        if m >= max_MSE:
            max_MSE = m
        if m <= best and no1 != no2:
            best = m
            best_name = no2
        if m > best and m <= snd_best and no1 != no2:
            snd_best = m
            snd_best_name = no2
        if no1 == no2:
        #if fn_enrol == fn_scan:
            #print(str(no1) + " and "+str(no2))
            T+=1
            if m < correct:
                correct = m
                correct_name = no2
            labels.append((m,True))
        else:
            F+=1
            labels.append((m,False))
    gen_best_snd.append([correct,best,snd_best])
    if correct >= best:
        print("for "+str(no1)+ ": smallest: "+str(best_name)+" with "+str(best) + \
           " whereas correct: "+str(correct_name)+ "with "+str(correct))
    #else: pass
        #print("for "+str(no1)+ ": smallest: "+str(best_name)+" with "+str(best) + \
        #     " 2nd smallest: "+str(snd_best_name)+ "with distance:"+str(snd_best-best))

    #print("smallest: "+str(best))
    #print("correct: "+str(correct))
    else:
    #if correct < best:
        correct_best_hits += 1

max_MSE = int(max_MSE)
#print "Done."
#print "True Samples: "+str(T)
#print "False Samples: "+str(F)
#print "Maximum MSE: "+str(max_MSE)
print("recognition rate: "+str(correct_best_hits) + "/"+str(len(enrols))+": "+str(round(correct_best_hits/float(len(enrols)),3)))

numpy.save("rec_perf.npy",numpy.array([correct_best_hits, len(enrols)]))

# Calculate ROC Statistic
x = []
y = []

threshold = 0.0

print "Calculating ROC Statistic. This may take a few minutes, depending on the sample size..."
#rocfile = open(INPUT_FILE_ORIGINAL+"_ROC","w")
#rocfile.close()

print("max mse"+str(max_MSE))
while threshold <= max_MSE:
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    P = T
    N = F
    
    # Calculate statistic for this threshold
    for (h,l) in labels: 
        if h >= threshold:
            if l:
                FN+=1
            else:
                TN+=1
        else:
            if l:
                TP+=1
            else:
                FP+=1
    
    fpr = float(FP)/(float(FP)+float(TN))
    tpr = float(TP)/(float(TP)+float(FN))
    x.append(fpr)
    y.append(tpr)
    
    #print "Thresh: "+str(threshold)+"; P: "+str(P)+"; TP: "+str(TP)+"; FP: "+str(FP)+"; N: "+str(N)+"; TN: "+str(TN)+"; FN: "+str(FN)+"; TPR: "+str(tpr)+"; FPR: "+str(fpr)
    # rocfile = open(statfile+"_ROC","a")
    # rocfile.write("Thresh: "+str(threshold)+"; P: "+str(P)+"; TP: "+str(TP)+"; FP: "+str(FP)+"; N: "+str(N)+"; TN: "+str(TN)+"; FN: "+str(FN)+"; TPR: "+str(tpr)+"; FPR: "+str(fpr)+"\n")
    # rocfile.close()

    threshold += max_MSE/float(PRECISION)

numpy.save("xy.npy", [x,y])

pyplot.plot(x,y)
pyplot.xscale('log')          
pyplot.show()

x_stats = range(0,len(enrols))
y_stats1 = [x[0] for x in gen_best_snd]
y_stats2 = [x[1] for x in gen_best_snd]
y_stats3 = [x[2] for x in gen_best_snd]
print(str(len(fn_enrol)) + " "+str(len(y_stats1)) + " "+str(len(y_stats2)))

pyplot.plot(x_stats,y_stats1,'o',x_stats,y_stats2,'v')
pyplot.show()

numpy.save("xy_stats.npy",[x_stats,y_stats1,y_stats2,y_stats3])
# Plot the results             
#pl.clf()                                            # Clear Plot
#pl.plot([0, 1], [0, 1], 'k--')                      # Plot Middle Line (Marks randomness)
#pl.xlim([0.0, 1.0])
#pl.semilog(np.exp(np.arange(10)))
#pl.ylim([0.0, 1.0])   
#pl.xlabel('False Positive Rate')
#pl.ylabel('True Positive Rate')
#pl.title(TITLE)
#pl.semilogx(x, y, label=": Area = %f"%auc(x, y), linestyle = "steps")
#pl.xscale('log')
#pl.legend(loc="lower right")
#pl.show()
