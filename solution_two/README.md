# Python Memory optimisation programme

A project developed for optimising Memory spikes of of a certain given code snippet

Requirements:
* Python 3.6 
* memory-profiler for profiling memory usage

v1 - given code
v2- optimised code reduced memory consumption by 50 %,by concatinating dataframes in run method of class pipeline
v3- optimised code reduced memory consumption by 70 % ,by creating a list of dataframes and and merging them together

you can run the python file named can2 and can3 individually.

python can2.py
python can3.py

Memory Profifer
import memory_profiler and tag the following decorator to individual methods

fp = open('memory_profiler_basic_mean.log', 'w+')
@profile(precision=precision, stream=fp)

python -m memory_profiler can2.py
python -m memory_profiler can3.py