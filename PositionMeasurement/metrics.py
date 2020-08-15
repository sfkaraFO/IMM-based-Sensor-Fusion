import numpy as np


def REES(xTrue,xFilt,P):
    res = xTrue - xFilt
    N,_,_ = res.shape
    val = 0
    for i in range(N):    
        val = val + res[i,:,:].T.dot(np.linalg.inv(P[i,:,:])).dot(res[i,:,:])
    val = val/N
    return val
	

def RMSE(xTrue,xFilt):
    N,_,_ = xTrue.shape
    res = xTrue - xFilt
    val = np.sqrt(np.sum(np.square(res),0)/N)
    return val


def NIS(xTrue,xFilt,P):
    a = 0
    return a
    
