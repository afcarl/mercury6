A.S. - three additional scripts created to aid use:
1) compile.sh - run “sh compile.sh” to compile all the necessary packages.
2) clean.sh - run “sh clean.sh” to clean the folder of the previous run. It may be true that every time you want to run a new run you need to first run clean.sh and then compile.sh
3) analysis.sh - run “analysis.sh” to extract the orbital parameters from the data files, move them to analysis/ folder, and calculate the energy. 

This tar file contains all the files necessary to compile
 and run the Mercury N-body integrator package, version 6.2. 
 The following files should be present:

 big.in
 close.in
 close6.for
 element.in
 element6.for
 files.in
 mercury.inc
 mercury6.man
 mercury6_2.for
 message.in
 param.in
 small.in
 swift.inc

 Start by looking at the manual contained in mercury6.man

 mercury6_2.for contains the source code for the integrator.
 element6.for contains source code for a programme to turn
   compressed output from mercury into coordinates or orbital
   elements for each object.
 close6.for contains source code for a programme to provide
   details on close encounters during an integration.

