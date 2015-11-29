echo "Extracting data files and calculating energy"
./element6

rm analysis/*.aei
mv *.aei elapsed_time.txt analysis/.
python calc_energy.py analysis/
