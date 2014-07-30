from parsing import *
from spike_train_object import *

"""
This script imports the fly experiment data for the 200 repeats of the 
5 sec stimulus.

It loads the runs as SpikeTrain objects and shifts all their starting 
times to 0.

Use this to setup the spike trains to analyse them, to avoid having to 
do these steps manually.
"""

spike_times = np.loadtxt("./data/Sfly01508SpikeTimes.txt")
repeated_exp = split_into_runs(spike_times, 200, 1000)

spike_trains = [SpikeTrain(i, end_time=5) for i in repeated_exp]

for s in spike_trains:
    s.shift_start_time(0)
    s.make_time_array(time_resolution=0.0001) #micro second resolution