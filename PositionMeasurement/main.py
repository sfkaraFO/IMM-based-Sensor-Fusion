# from filterpy.stats import plot_covariance_ellipse
import matplotlib.pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
import numpy as np
# import txt_gen as txt

import sensor_fusion as fuse

from generate_sensor_meas import GenerateData
from metrics import REES
from metrics import RMSE
from sys_def import SysDef


plt.close('all')

CVModel = SysDef()

### Simulate measurement data ###
yD, yT1, yT2, yP, trueV = GenerateData(CVModel)

### Sensor Fusion algorithms ###
xI, covI, mus = fuse.IMMFusion(yD, yT1, yT2, yP, CVModel)



print ("Last Covariance IMM: \n", covI[-1,:,:])
print ("REES IMM: \n", REES(trueV, xI, covI))
print ("RMSE IMM: \n", RMSE(trueV, xI))

tt = np.arange(0,CVModel.Tfinal,CVModel.Ts)
plt.subplot(131)
p1 = plt.plot(tt, trueV[:,0,0],'-.')
p3 = plt.plot(tt, xI[:,0,0])
plt.legend(['True Value','IMM Estimate'])
plt.xlabel('Time(s)')
plt.ylabel('Position(m)')
#plt.savefig('PositionPlot2.pdf')

plt.subplot(132)
p1 = plt.plot(tt, trueV[:,1,0],'-.')
#p2 = plt.plot(yD[0]/1000, yD[1]/Ndoppler, 'or')
#p2 = plt.plot(yT1[0]/1000, yT1[1]*Ntacho, 'ob')
#p2 = plt.plot(yT2[0]/1000, yT2[1]*Ntacho, 'og')
p4 = plt.plot(tt, xI[:,1,0])
plt.legend(['True Value','IMM Estimate'])
plt.xlabel('Time(s)')
plt.ylabel('Velocity(m/s)')
#plt.savefig('VelocityPlot2.pdf')

plt.subplot(133)
p4 = plt.plot(tt, mus[:,0])
p4 = plt.plot(tt, mus[:,1])
plt.legend(['Mode 1','Mode 2'])
plt.xlabel('Time(s)')
plt.ylabel('Mode')
#plt.savefig('ModePlot2.pdf')
plt.savefig('Total.pdf')

plt.show()























