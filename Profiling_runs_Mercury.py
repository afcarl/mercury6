#A.S. This clean's the directory, recompiles the directory, and then runs mercury, keeping time in the process.
import multiprocessing as mp
from subprocess import call
import os
import sys
import time

def execute(dir):
    call('cp mercury6_2.for '+dir+'/.',shell=True)
    call('cp element6.for '+dir+'/.',shell=True)
    call('rm mercury_*.in '+dir+'/.',shell=True)
    call('cp *.in '+dir+'/.',shell=True)
    call('cp swift.inc '+dir+'/.',shell=True)
    call('cp clean.sh '+dir+'/.',shell=True)
    os.chdir(dir)
    call('sh clean.sh',shell=True)
    call('gfortran -o mercury6 mercury6_2.for',shell=True)
#    call('gfortran -o element6 element6.for',shell=True)
    call('rm eo.txt ET.txt',shell=True)
    call('touch eo.txt',shell=True)
    start = time.time()
    #call('./mercury6', shell=True)
    call('./mercury6 > eo.txt',shell=True)
    f = open('ET.txt','w')
    f.write('Elapsed time is %f seconds.'%(time.time() - start))
    f.close()

if __name__== '__main__':
    files = [x[0] for x in os.walk('input_files/')][1:]
    N_procs = 1           #might need to be changed in the future. 
    pool = mp.Pool(processes=N_procs)
    args=[files[i] for i in xrange(0,len(files))]
    print args
    pool.map(execute, args)
    pool.close()
    pool.join()
