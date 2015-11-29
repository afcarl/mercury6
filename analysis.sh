echo "Extracting data files and calculating energy"
./element6

mv *.aei analysis/.
mv eo.txt elapsed_time.txt analysis/.
python calc_energy.py analysis/
