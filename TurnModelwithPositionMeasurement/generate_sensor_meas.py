import numpy as np
from numpy.random import randn


def GenerateData(sys): 
    
    yDoppler = []
    yTacho1 = []
    yTacho2 = []
    yTag    = []
    trueVal = []
    trueVal2 = []

    # Generate Measurements
    stdAcc = 0.1
    pos,vel,acc = 0,0,0
    PosX, PosY, VelX, VelY, AccX, AccY = 0,0,2,0,0,0
    posPre = 0
    for t in np.arange(0,sys.Tfinal,sys.Ts):

        if t < 4:
            AccX = 0
            AccY = 0
        elif t < 24:
            AccX = -.1
            AccY = .1
        elif t < 28:
            AccX = 0
            AccY = 0
        elif t < 48:
            AccX = -.1
            AccY = -.1           
        else:
            AccX = 0
            AccY = 0

        #acc = u + randn()*stdAcc
        #vel = vel + acc*sys.Ts
        #pos = pos + vel*sys.Ts
        VelX = VelX + AccX*sys.Ts
        VelY = VelY + AccY*sys.Ts
        PosX = PosX + VelX*sys.Ts
        PosY = PosY + VelY*sys.Ts
        trueVal2.append([PosX, PosY])

        #vel = np.sqrt(VelX*VelX + VelY*VelY)
        pos = np.sqrt(PosX*PosX + PosY*PosY)
        vel = (pos - posPre)/sys.Ts
        trueVal.append([pos, vel])

        yDoppler.append([(t+0.010)*1000, vel*sys.Ndoppler + randn()*sys.stdDoppler])
        yTacho1.append([(t+0.020)*1000, vel*sys.Ntacho + randn()*sys.stdTacho])
        yTacho2.append([(t+0.030)*1000, vel*sys.Ntacho + randn()*sys.stdTacho])
        #yTag.append([t, pos*sys.Ntag + randn()*sys.stdTag])
        if t%3 < 0.001:
            yTag.append([t, pos*sys.Ntag + randn()*sys.stdTag])
        else:
            yTag.append([-1, -1]) 
        posPre = pos
        
    yD = np.asarray(yDoppler).T
    yT1 = np.asarray(yTacho1).T
    yT2 = np.asarray(yTacho2).T
    yP = np.asarray(yTag).T
    ttrueVal = np.asarray(trueVal)
    ttrueVal = ttrueVal.reshape(-1,2,1)
    
    ttrueVal2 = np.asarray(trueVal2)
    ttrueVal2 = ttrueVal2.reshape(-1,2,1)

    return yD, yT1, yT2, yP, ttrueVal, ttrueVal2 
 
