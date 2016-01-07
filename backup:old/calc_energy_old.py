#A.S. Calc energy of mercury6. But there is a way to just output it from mercury.

import glob
import numpy as np
import re
import matplotlib.pyplot as plt
import sys

def get_com(cube, iteration, N_bods):
    com = np.zeros(7) #m,x,y,z,vx,vy,vz
    com[0] += 1     #sun's mass = 1
    for i in xrange(0,N_bods):
        m = cube[i][iteration][1]
        com[1] += m*cube[i][iteration][2] #x
        com[2] += m*cube[i][iteration][3] #y
        com[3] += m*cube[i][iteration][4] #z
        com[4] += m*cube[i][iteration][5] #vx
        com[5] += m*cube[i][iteration][6] #vy
        com[6] += m*cube[i][iteration][7] #vz
        com[0] += m
    if com[0] > 0:
        com[1] /= com[0]
        com[2] /= com[0]
        com[3] /= com[0]
        com[4] /= com[0]
        com[5] /= com[0]
        com[6] /= com[0]
    return com

def get_energy(cube, com, iteration, N_bods):
    K = 0
    U = 0
    G = 0.025330296   #G=1 units?
    K += 0.5*(com[4]*com[4] + com[5]*com[5] + com[6]*com[6])   #sun non-zero in COM frame
    for i in xrange(0,N_bods):
        mi = cube[i][iteration][1]
        dx = cube[i][iteration][2]
        dy = cube[i][iteration][3]
        dz = cube[i][iteration][4]
        dvx = cube[i][iteration][5] - com[4]
        dvy = cube[i][iteration][6] - com[5]
        dvz = cube[i][iteration][7] - com[6]
        r = (dx*dx + dy*dy + dz*dz)**0.5
        if r!=r:
            print 'nan value at', i
            exit(0)
        U -= G*mi/r                                        #U_sun/massive body
        K += 0.5*mi*(dvx*dvx + dvy*dvy + dvz*dvz)               #KE body
        for j in xrange(i+1,N_bods):
            mj = cube[j][iteration][1]
            ddx = dx - cube[j][iteration][2]
            ddy = dy - cube[j][iteration][3]
            ddz = dz - cube[j][iteration][4]
            r = (ddx*ddx + ddy*ddy + ddz*ddz)**0.5
            U -= G*mi*mj/r                                  #U between bodies
    return U + K

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

files = glob.glob('*.aei')
files = sorted(files, key=natural_key)
N_bodies = len(files)

#file 0 is the sun which is empty
cube=np.genfromtxt(files[0],delimiter=' ',skiprows = 4, dtype=float)
nr, nc = cube.shape
cube = np.reshape(cube, (1,nr,nc))

#read in data for each body
for i in xrange(1,N_bodies):
    data=np.genfromtxt(files[i],delimiter=' ',skiprows = 4, dtype=float)
    data = np.reshape(data, (1,nr,nc))
    cube = np.concatenate((cube,data),axis=0)

N_bods,N_output,N_cols = cube.shape

#calc E of system at time 0
dE = np.zeros(N_output)
time = np.zeros(N_output)
com = get_com(cube,0,N_bods)
E0 = get_energy(cube,com,0,N_bods)
for i in xrange(0,N_output):
    com = get_com(cube,i,N_bods)
    E = get_energy(cube,com,i,N_bods)
    dE[i] = np.fabs((E - E0)/E0)
    time[i] = cube[0][i][0]

plt.plot(time, dE, 'o')
plt.yscale('log')
plt.xscale('log')
plt.savefig(dir+'Energy.png')
plt.show()

