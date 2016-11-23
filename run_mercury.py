#A.S. This clean's the directory, recompiles the directory, and then runs mercury, keeping time in the process.
from subprocess import call
import time

call("sh clean.sh",shell=True)
call("sh compile.sh",shell=True)
call("rm eo.txt",shell=True)
call("touch eo.txt",shell=True)

call("gfortran -o mercury6 mercury6_2.for",shell=True)
call("./mercury6")