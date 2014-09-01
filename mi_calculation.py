from spike_train_object import *
from parsing import *
import numpy as np
#import scipy as sci
#import sys

"""
This script should be passes parameters at run time:
the order should be: number_of_trials(experiments), number_of_stimuli, nh
"""

#n_trials = 20
#nh = 10


#n_trials = int(sys.argv[1])
#n_stim = int(sys.argv[2])
#nh = int(sys.argv[3])

#t_stim = 5.0/n_stim


spike_times = np.loadtxt("./data/Sfly01508SpikeTimes.txt")
#repeated_exp = split_into_runs(spike_times, 200, 1000)


n_trials_list = range(10,20,1)
n_stim_list = range(5,26,5)




Mutual_Information = []
NT = []
NS = []


for n_trials in n_trials_list:
    for n_stim in n_stim_list:
        
        t_stim = 5.0/n_stim
        
        repeated_exp = split_into_runs(spike_times, 200, 1000)
        repeated_exp_used = repeated_exp[:n_trials]
        repeated_exp_used = [repeated_exp_used[i] - 5*i for i in range(len(repeated_exp_used))]

        more_splitting = np.array([split_into_runs(run, n_stim, 5) for run in repeated_exp_used])
        responses = [[SpikeTrain(e[i], t_stim*i, t_stim*i + t_stim ) for i in range(len(e))] for e in more_splitting]

        responses = np.array(responses).flatten()

        DM = make_distance_matrix(responses)
        nearest_neighbours = np.array([r.argsort()[:nh] for r in DM])

        counts = []
        for i in range(len(nearest_neighbours)):
            c_i = 0
            for j in nearest_neighbours[i]:
                if responses[i].start_time == responses[j].start_time:
                    c_i += 1 
            counts.append(c_i)
        counts = np.array(counts)
            
        ns = 20


        I = sum(np.log2(counts*ns/float(nh)))

        NT.append(n_trials)
        NS.append(n_stim)
        Mutual_Information.append(I)
        
head = ["number of trials", "number of stimuli", "mutual information"]
data = np.column_stack((NT, NS, Mutual_Information))
#data = np.row_stack((head, data))
np.savetxt("data_mutual_info.dat", data)