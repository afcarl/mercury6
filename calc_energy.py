#A.S. This just reads in the mercury6 calculated energies and plots it.

import numpy as np
import matplotlib.pyplot as plt
import sys

dir = sys.argv[1]

#energy offset
data=np.genfromtxt(dir+'eo.txt',delimiter=None, dtype=float)
nr, nc = data.shape
dE = np.zeros(nr)
time = np.zeros(nr)
for i in xrange(0,nr):
    dE[i] = abs(data[i][1])
    time[i] = data[i][0]*0.01721420632  #constant is 2pi/365


plt.plot(time,dE,'o')
plt.yscale('log')
plt.xscale('log')
plt.savefig(dir+'Energy.png')
plt.show()

