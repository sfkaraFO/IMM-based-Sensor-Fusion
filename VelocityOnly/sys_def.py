# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 07:51:04 2020

@author: geminix
"""

import numpy as np

class SysDef(object):
     
    def __init__(self):
        self.Ts = 0.1
        self.Tfinal = 25
        self.Ndoppler = 1 
        self.Ntacho   = 25  #Pulse to meter for Tachometer
        self.stdDoppler = 0.1
        self.stdTacho = 10
        self.Htotal = np.array([[0,self.Ndoppler],[0,self.Ntacho],[0,self.Ntacho]])
        self.Rtotal = np.array([[self.stdDoppler**2,0,0],[0,self.stdTacho**2,0],[0,0,self.stdTacho**2]])
        #self.Hdoppler = np.array([[0,self.Ndoppler]])
        #self.Htacho = np.array([[0,self.Ntacho]])  
        #self.Rdoppler = np.array([[self.stdDoppler**2]])
        #self.Rtacho = np.array([[self.stdTacho**2]])

                             
    def F(self, dt):  
        return np.array([[1., dt],[0., 1.]])
    
    def Q(self, dt,mu):
        if mu==1:
            c = .1
        elif mu==2: 
            c = 15
        else:
            print("Process noise error!!")
            
        return np.array([[dt**4/4, dt**3/2],[dt**3/2, dt**2]])*c

        

        
    
       
   
    
    
    


