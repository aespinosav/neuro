from parsing import *
from spike_train_object import *
import numpy as np


spike_times = np.loadtxt("./data/Sfly01508SpikeTimes.txt")

n_trials_list = range(10,20,1)
n_stim_list = range(10,46,5)

print "\nWill calculate {} Distance Matrices...".format(len(n_trials_list)*len(n_stim_list))

count = 1
for n_trials in n_trials_list:
    for n_stim in n_stim_list:
        
        print "\nLoop ", count
        print "nt = {}; ns = {}\n".format(n_trials, n_stim)
        
        
        t_stim = 5.0/n_stim
        
        repeated_exp = split_into_runs(spike_times, 200, 1000)
        repeated_exp_used = repeated_exp[:n_trials]
        repeated_exp_used = [repeated_exp_used[i] - 5*i for i in range(len(repeated_exp_used))]
        
        more_splitting = np.array([split_into_runs(run, n_stim, 5) for run in repeated_exp_used])
        responses = [[SpikeTrain(e[i], t_stim*i, t_stim*i + t_stim ) for i in range(len(e))] for e in more_splitting]

        responses = np.array(responses).flatten()

        DM = make_distance_matrix(responses)
        
        filename = "dist_matrix_ns_{0}_nt_{1}.dat".format(n_stim, n_trials)
        
        np.savetxt(filename, DM)
        
        count+=1