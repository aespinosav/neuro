import numpy as np
from spike_train_object import *
from parsing import *
from collections import Counter
import re


def load_spike_trains(directory, ns, nt):
    
    spike_times = np.loadtxt(directory + "Sfly01508SpikeTimes.txt")
    repeated_exp = split_into_runs(spike_times, 200, 1000)
    repeated_exp_used = repeated_exp[:nt]
    spike_trains = [repeated_exp_used[i] - 5*i for i in range(len(repeated_exp_used))]
    
    t_stim = 5.0/ns
    
    responses = np.array([split_into_stimuli(experiment, 5,  ns) for experiment in spike_trains])
    responses_trains = np.array([[SpikeTrain(e[i], t_stim*i, t_stim*(1 + i)) for i in range(len(e))] for e in responses])
    
    
    return responses_trains.flatten()
    

def import_stuff(f_name):
    
    directory_of_dist_mat = "/users/ae13414/Documents/neuro/data/dist_matrices3/"
    directory_of_spike_data = "/users/ae13414/Documents/neuro/data/"
    
    seq = filter(None, re.split("[_.]", f_name))
    ns = int(seq[seq.index('ns') + 1])
    nt = int(seq[seq.index('nt') + 1])

    nr = ns*nt
    
    dm = np.loadtxt(directory_of_dist_mat+f_name)
    
    spike_trains = load_spike_trains(directory_of_spike_data, ns, nt)
    
    return spike_trains, dm
    
    
def trains_in_glob(spike_trains):
    """
    Returns a list of all the trains in the glob
    
    se docstring of glob_composition on how to decide who is in the glob.
    """
    
    nr = len(spike_trains)

    trains = [i for i in range(nr) if len(spike_trains[i].spiking_times) == 0]

    return trains    


def glob_composition(spike_trains, ns, nt, nh):
    """
    Function returns a dictionary of the composition of the
    zero glob.
    
    There is a very big assumption here. That spikes trains that have more than 
    nh neighbours at zero distance are considered to be spike trains with no spikes.
    
    It works well so far! at least for large ns, which is what we are really interested
    in.
    """
    
    t_i_g = trains_in_glob(spike_trains)
    
    stims = [i%ns for i in t_i_g]
    
    glob_comp = Counter(stims)
    
    return glob_comp
