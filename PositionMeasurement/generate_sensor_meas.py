import numpy as np
from numpy.random import randn


def GenerateData(sys): 
    
    yDoppler = []
    yTacho1 = []
    yTacho2 = []
    yTag    = []
    trueVal = []
    
    # Generate Measurements
    stdAcc = 0.1
    pos,vel,acc = 0,0,0
    for t in np.arange(0,sys.Tfinal,sys.Ts):
        if t < 5:
            u = 2
        elif t < 10:
            u = 0
        elif t < 15:
            u = 2
        elif t < 20:
            u = 0
        elif t < 25:
            u = -4
        else:
            u = 0
            
        acc = u + randn()*stdAcc
        vel = vel + acc*sys.Ts
        pos = pos + vel*sys.Ts
        
        trueVal.append([pos,vel])
        yDoppler.append([(t+0.010)*1000, vel*sys.Ndoppler + randn()*sys.stdDoppler])
        yTacho1.append([(t+0.020)*1000, vel*sys.Ntacho + randn()*sys.stdTacho])
        yTacho2.append([(t+0.030)*1000, vel*sys.Ntacho + randn()*sys.stdTacho])
        if t%3 == 1:
            yTag.append([t, pos*sys.Ntag + randn()*sys.stdTag])
        else:
            yTag.append([-1, -1]) 
            #yTag.append([t, pos*sys.Ntag + randn()*sys.stdTag])
    
        
    yD = np.asarray(yDoppler).T
    yT1 = np.asarray(yTacho1).T
    yT2 = np.asarray(yTacho2).T
    yP = np.asarray(yTag).T
    ttrueVal = np.asarray(trueVal)
    ttrueVal = ttrueVal.reshape(-1,2,1)

    return yD, yT1, yT2, yP, ttrueVal 
