echo "Extracting data files and calculating energy"
./element6

mv *.aei analysis/.
python calc_energy.py analysis/
