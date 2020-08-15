import numpy as np
from scipy.linalg import inv
from scipy.stats import multivariate_normal

def NormalFusion(yD, yT1, yT2, sys):
    
    xs = []
    # Ozge's method
    for i,t in enumerate(np.arange(0,sys.Tfinal,sys.Ts)):
        xs.append((yD[1,i]*sys.Ndoppler + yT1[1,i]*sys.Ntacho + yT2[1,i]*sys.Ntacho)/3)
    
    return xs



class KalmanFilter(object):
    
    def __init__(self, c):
        self.c = c
        
    def TimeUpdate(self,dt,sys,x,P):
        x = sys.F(dt).dot(x)
        P = sys.F(dt).dot(P).dot(sys.F(dt).T) + sys.Q(dt,self.c)           
        return x,P
        
    def MeasUpdate(self,x,P,z,H,R):
        S = H.dot(P).dot(H.T) + R
        K = P.dot(H.T).dot(inv(S))
        y = z - H.dot(x)
        x = x + K.dot(y)
        P = P - K.dot(H).dot(P)
        return x,P
    
    




def KalmanFusion(yD, yT1, yT2, sys):

    x0 = np.array([[0],[0]])
    P0 = np.array([[100,0],[0,100]]) 
    x = x0
    P = P0
    xs, cov = [], []

    KF = KalmanFilter(1)
    
    for i,t in enumerate(np.arange(0,sys.Tfinal,sys.Ts)):
        
        # predict
        dt = 0.1
        x,P = KF.TimeUpdate(dt,sys,x,P)
        
        z = np.array([[yD[1][i]],[yT1[1][i]],[yT2[1][i]]])
        H = sys.Htotal
        R = sys.Rtotal
        
        #update
        x,P = KF.MeasUpdate(x,P,z,H,R)
    
        xs.append(x)
        cov.append(P)
             
        
        
    xs = np.asarray(xs)
    cov = np.asarray(cov)
    
    return xs, cov



def IMMFusion(yD, yT1, yT2, sys):
       
    x0 = np.array([[0],[0]])
    P0 = np.array([[100,0],[0,100]]) 
    x1 = x0
    P1 = P0
    x2 = x0
    P2 = P0
    xs, cov = [], []
    mus = []
    mu = np.array([0.01, 0.99])
    mu1 = np.array([0.,0.])
    mu2 = np.array([0.,0.])

    piMat = np.array([[0.9,0.1],[0.1,0.9]])

    KF1 = KalmanFilter(1)
    KF2 = KalmanFilter(2)
    
    for i,t in enumerate(np.arange(0,sys.Tfinal,sys.Ts)):
        # i = 1, Model-1      
        mu1[0] = piMat[0,0]*mu[0]
        mu1[1] = piMat[1,0]*mu[1]  
        normSum = mu1[0] + mu1[1]
        mu1[0] = mu1[0] / normSum
        mu1[1] = mu1[1] / normSum
        
        x01 = mu1[0]*x1 + mu1[1]*x2
        P01 = mu1[0]*(P1 + (x1-x01).dot((x1-x01).T)) \
                + mu1[1]*(P2 + (x2-x01).dot((x2-x01).T))
        
        # i = 2, Model-2
        mu2[0] = piMat[0,1]*mu[0]
        mu2[1] = piMat[1,1]*mu[1]  
        normSum = mu2[0] + mu2[1]
        mu2[0] = mu2[0] / normSum
        mu2[1] = mu2[1] / normSum
        
        x02 = mu2[0]*x1 + mu2[1]*x2
        P02 = mu2[0]*(P1 + (x1-x02).dot((x1-x02).T)) \
                + mu2[1]*(P2 + (x2-x02).dot((x2-x02).T))
        
        # predict
        dt = 0.1
        x1,P1 = KF1.TimeUpdate(dt,sys,x01,P01)
        x2,P2 = KF2.TimeUpdate(dt,sys,x02,P02)

        z = np.array([[yD[1][i]],[yT1[1][i]],[yT2[1][i]]])
        H = sys.Htotal
        R = sys.Rtotal
        
        # Mode Propability Update
        likelihood1 = multivariate_normal(H.dot(x1).reshape(-1,), H.dot(P1).dot(H.T) + R)
        likelihood2 = multivariate_normal(H.dot(x2).reshape(-1,), H.dot(P2).dot(H.T) + R)
        mu[0] = likelihood1.pdf(z.reshape(-1,))*(piMat[0,0]*mu[0] + piMat[1,0]*mu[1])
        mu[1] = likelihood2.pdf(z.reshape(-1,))*(piMat[0,1]*mu[0] + piMat[1,1]*mu[1])
        normSum2 = mu[0] + mu[1]
        mu[0] = mu[0]/normSum2
        mu[1] = mu[1]/normSum2
        
        #update
        x1,P1 = KF1.MeasUpdate(x1,P1,z,H,R)
        x2,P2 = KF1.MeasUpdate(x2,P2,z,H,R)


        
        x = mu[0]*x1 + mu[1]*x2
        P = mu[0]*(P1 + (x1-x).dot((x1-x).T)) \
                + mu[1]*(P2 + (x2-x).dot((x2-x).T))



        xs.append(list(x))
        cov.append(list(P))
        mus.append(list(mu))
        
             
        
    
    xs = np.asarray(xs)
    cov = np.asarray(cov)
    mus = np.asarray(mus)
   
    return xs, cov, mus




