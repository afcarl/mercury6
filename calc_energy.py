#A.S. This actually calculates the energy based on the outputted xyz and vx,vy,vz positions/velocities
#Symba only uses massless particles, and so there is no particle-particle interactions!!
#Python note: genfromtxt only makes a 2D array if all the elements are of the same type. Otherwise what I get is called a "structured ndarray". Makes it hard to concatenate and stuff, though it can still work with np.dstack.

import glob
import numpy as np
import re
import matplotlib.pyplot as plt
import sys

def h2b(cube, m0, iteration, N_bodies, mtiny):  #heliocentric to barycentric
    day2AU = 58.13134242
    com = np.zeros(7) #m,x,y,z,vx,vy,vz
    m = np.zeros(N_bodies+1)
    m[0] = m0
    com[0] += m0       #sun's mass
    for i in xrange(1,N_bodies+1):
        m[i] = cube[i-1][iteration][1]
        if m[i] > mtiny:
            com[1] += m[i]*cube[i-1][iteration][2] #x
            com[2] += m[i]*cube[i-1][iteration][3] #y
            com[3] += m[i]*cube[i-1][iteration][4] #z
            com[4] += m[i]*cube[i-1][iteration][5]*day2AU #vx
            com[5] += m[i]*cube[i-1][iteration][6]*day2AU #vy
            com[6] += m[i]*cube[i-1][iteration][7]*day2AU #vz
            com[0] += m[i]
    #print cube[i-1][iteration][1], cube[i-1][iteration][2],cube[i-1][iteration][3], cube[i-1][iteration][4], cube[i-1][iteration][5], cube[i-1][iteration][6], cube[i-1][iteration][7]
    x = np.zeros(N_bodies+1)
    y = np.zeros(N_bodies+1)
    z = np.zeros(N_bodies+1)
    vx = np.zeros(N_bodies+1)
    vy = np.zeros(N_bodies+1)
    vz = np.zeros(N_bodies+1)
    x[0] = -com[1]/com[0]
    y[0] = -com[2]/com[0]
    z[0] = -com[3]/com[0]
    vx[0] = -com[4]/com[0]
    vy[0] = -com[5]/com[0]
    vz[0] = -com[6]/com[0]
    for i in xrange(1,N_bodies+1):
        x[i] = cube[i-1][iteration][2] + x[0]
        y[i] = cube[i-1][iteration][3] + y[0]
        z[i] = cube[i-1][iteration][4] + z[0]
        vx[i] = cube[i-1][iteration][5]*day2AU + vx[0]
        vy[i] = cube[i-1][iteration][6]*day2AU + vy[0]
        vz[i] = cube[i-1][iteration][7]*day2AU + vz[0]
    return m, x, y, z, vx, vy, vz

def cal_energy(m,x,y,z,vx,vy,vz,N_bodies,mtiny):
    K = 0
    U = 0
    G = 1   #G=1 units
    for i in xrange(0,N_bodies+1):
        K += 0.5*m[i]*(vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i])     #KE body
        if m[i] > mtiny:                    #ignore forces between planetesimals
            for j in xrange(i+1,N_bodies+1):
                dx = x[i] - x[j]
                dy = y[i] - y[j]
                dz = z[i] - z[j]
                r = (dx*dx + dy*dy + dz*dz)**0.5
                U -= G*m[i]*m[j]/r          #U between bodies
    return U + K

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

dir = sys.argv[1]
files = glob.glob(dir+'*.aei')
files = sorted(files, key=natural_key)
N_bodies = len(files)

default_m0 = '1'
input = raw_input('Enter Suns mass (default, Msun=1): ')
if not input:
    m0 = float(default_m0)
else:
    m0 = float(input)

default_mtiny = '1e-07'
input = raw_input('Enter planetesimal mass (mtiny) value (default, mtiny=1e-07): ')
if not input:
    mtiny = float(default_mtiny)
else:
    mtiny = float(input)

cube=np.genfromtxt(files[0],delimiter=None,skiprows = 4, dtype=float)
nr, nc = cube.shape
cube = np.reshape(cube, (1,nr,nc))

#read in data for each body
for i in xrange(1,N_bodies):
    data=np.genfromtxt(files[i],delimiter=None,skiprows = 4, dtype=float)
    data = np.reshape(data, (1,nr,nc))
    cube = np.concatenate((cube,data),axis=0)

N_bods,N_output,N_cols = cube.shape

#calc E of system at time 0
dE = np.zeros(N_output)
time = np.zeros(N_output)
m,x,y,z,vx,vy,vz = h2b(cube,m0,0,N_bodies,mtiny)
E0 = cal_energy(m,x,y,z,vx,vy,vz,N_bodies,mtiny)
print 'calculating energy'
increment = 0.1*N_output
for i in xrange(1,N_output):
    m,x,y,z,vx,vy,vz = h2b(cube,m0,i,N_bodies,mtiny)
    E = cal_energy(m,x,y,z,vx,vy,vz,N_bodies,mtiny)
    dE[i] = np.fabs((E - E0)/E0)
    time[i] = cube[0][i][0]
    if i > increment:
        print '% done =',round(100*float(i)/float(N_output))
        increment += 0.1*N_output

plt.plot(time, dE, 'o')
plt.yscale('log')
plt.xscale('log')
plt.savefig(dir+'Energy.png')
plt.show()
