#A.S. This clean's the directory, recompiles the directory, and then runs mercury, keeping time in the process.
from subprocess import call
import time

call("sh clean.sh",shell=True)
call("sh compile.sh",shell=True)
call("rm eo.txt",shell=True)
call("touch eo.txt",shell=True)

start_time = time.time()

call("./mercury6")

elapsed_time = time.time() - start_time
print 'elapsed time =',elapsed_time
fos = open('elapsed_time.txt','w')
fos.write('elapsed time = '+str(elapsed_time))