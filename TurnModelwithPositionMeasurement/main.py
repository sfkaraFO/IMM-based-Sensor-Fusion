# Turn Model with Position measurements
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

## Simulate measurement data ###
yD, yT1, yT2, yP, trueV, trueV2 = GenerateData(CVModel)

### Sensor Fusion algorithms ###
xI, covI, mus = fuse.IMMFusion(yD, yT1, yT2, yP, CVModel)
#xI, covI = fuse.KalmanFusion(yD, yT1, yT2, yP, CVModel)



#print ("Last Covariance IMM: \n", covI[-1,:,:])
#print ("REES IMM: \n", REES(trueV, xI, covI))
#print ("RMSE IMM: \n", RMSE(trueV, xI))

tt = np.arange(0,CVModel.Tfinal,CVModel.Ts)

fig1 = plt.figure()
ax1 = fig1.add_subplot(121)
ax1.plot(trueV2[:,0,0], trueV2[:,1,0])
#plt.subplot(121)
#p1 = plt.plot(trueV2[:,0,0], trueV2[:,1,0])
plt.xlabel('x[m]')
plt.ylabel('y[m]')
plt.grid()

#plt.subplot(122)
#p2 = plt.plot(tt, trueV[:,0,0], linewidth=4, linestyle='-.')
#p2 = plt.plot(tt, xI[:,0,0], color='r', linewidth=4, linestyle=':')

ax2 = fig1.add_subplot(122)
ax2.plot(tt, trueV[:,0,0], linewidth=4, linestyle='-.')
ax2.plot(tt, xI[:,0,0], color='r', linewidth=4, linestyle=':')
ax2.axis(xmin=0,xmax=50,ymin=-5,ymax=55)
plt.xlabel('Time(s)')
plt.ylabel('Position(m)')
plt.grid()

ax3 = plt.axes([.79, .55, .2, .2])
ax3.plot(tt[350:499], trueV[350:499,0,0], linewidth=4, linestyle='-.')
ax3.plot(tt[350:499], xI[350:499,0,0], color='r', linewidth=4, linestyle=':')
ax3.axis(xmin=38,xmax=44,ymin=48,ymax=50)
ax3.set_yticklabels([])
plt.grid()

ax4 = plt.axes([.63, .15, .2, .2])
ax4.plot(tt[0:149], trueV[0:149,0,0], linewidth=4, linestyle='-.')
ax4.plot(tt[0:149], xI[0:149,0,0], color='r', linewidth=4, linestyle=':')
ax4.axis(xmin=6,xmax=9,ymin=12,ymax=16)
ax4.set_yticklabels([])
plt.grid()

#plt.setp(ax2, xticks=[], yticks=[])
#p2 = plt.plot(yP[0], yP[1], 'og')
#plt.legend(['True Value','IMM Estimate'])


plt.savefig('Turn.pdf')

plt.show()























