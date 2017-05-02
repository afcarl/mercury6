#A.S. This just reads in a collection of mercury6 runs, calculates energies and plots it.

import numpy as np
import matplotlib.pyplot as plt
import sys
import glob

dir = sys.argv[1]
files = glob.glob('%s/*/*eo.txt'%dir)

colors = ['black','brown','red','chocolate','orange','gold','green','dodgerblue','blue','purple']

#energy offset
for i,f in enumerate(files):
    data = np.genfromtxt(f, delimiter=None, dtype=None, skip_header=2, skip_footer=2)
    junk, time, junk, junk, dE, junk, dL, Np = zip(*data.T)
    HSF = f.split('HSF')[1].split('_')[0]
    plt.plot(time, dE, '.', color=colors[i], label='HSF=%s'%HSF)

plt.legend(loc='lower right', fontsize=10)

plt.plot(time,dE,'o')
plt.plot(time,1e-7*np.sqrt(time))
plt.yscale('log')
plt.xlabel('time')
plt.ylabel('Energy')
plt.savefig('%sEnergyplot.png'%dir)
plt.show()

