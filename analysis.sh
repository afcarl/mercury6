echo "Extracting data files and calculating energy"
./element6

rm output/*.aei
mv *.aei output/.
mv eo.txt elapsed_time.txt output/.
python calc_energy.py output/
