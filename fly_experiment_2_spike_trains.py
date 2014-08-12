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

spike_trains = [SpikeTrain(i,start_time=0, end_time=5) for i in repeated_exp]

for s in spike_trains:
    s.shift_start_time(0)
    s.make_time_array(time_resolution=0.0001) #micro second resolution
    s.kernelise(boxcar, 0.03)
    
dist_matrix = np.array([[distance(spike_trains[i], spike_trains[j]) for i in range(len(spike_trains))] for j in range(len(spike_trains))])

def kernel(i, j, nh):
    if dist_matrix(i,j) < nh:
        return 1.0/nh
    else:
        return 0
        
def counts_func(i, h):
    c = dist_matrix[i][dist_matrix[i] < h]
    return len(c)
    
nh = 30.

counts = []
for i in range(len(spike_trains)):
    for j in range(len(spike_trains)):
        c = counts_func(i, nh)
        counts.append(c)

I = 0
for i in range(len(spike_trains)):
    I += np.log2(counts[i]/nh)
I /= len(spike_trains)

