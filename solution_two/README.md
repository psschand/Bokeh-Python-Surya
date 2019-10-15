# Python Memory optimisation programme

A project developed for optimising Memory spikes of of a certain given code snippet

Requirements:
* Python 3.6 
* memory-profiler for profiling memory usage

v1 - given code
v2- optimised code reduced memory consumption by 50 %,by concatinating dataframes in run method of class pipeline
v3- optimised code reduced memory consumption by 70 % ,by creating a list of dataframes and and merging them together
# ---------------------

v3- updated the code used generators ,numpy arrays and garbage collection for better performance and stability
    I also added pickling and and unpickiling to reduce memory usage, The only problem I am facing here is deserialising 
    the compressed array.
v4- The same as v3 without the compressed array     
     divided numpy array in chunks ,and merged data frames along with  pickling and unpickling
     to optimise memory usage 
you can run the python file named can3.py and can4.py individually.

python can3.py
python can4.py

