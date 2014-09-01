"""
Script for plotting discretisation example.
Will plot n_trials spike trains and show how the first word is generated
for those many trials, if more than 10 trials are wanted you must adjust the 
text size
"""
from parsing import *
from spike_train_object import *

n_trials = 5
f_size = 16 #fontsize

spike_times = np.loadtxt("./data/Sfly01508SpikeTimes.txt")
repeated_exp = split_into_runs(spike_times, 200, 1000)
repeated_exp_used = repeated_exp[:n_trials]
trials = [repeated_exp_used[i] - 5*i for i in range(len(repeated_exp_used))]


st_tr = [SpikeTrain(t) for t in trials]

for s in st_tr:
    s.shift_start_time()

plot_trains_raster(st_tr)

x = np.arange(0.003, 0.03, 0.003)
ymin = np.zeros(len(x)) 
ymax = np.ones(len(x))*(n_trials+1)

plt.vlines(x, ymin, ymax, linewidth=0.5)
plt.vlines(0.03, 0, n_trials +1, linewidth=2)
plt.vlines(0, 0, n_trials + 1, linewidth=2)

plt.xlim([0,0.063])
plt.ylim([0,n_trials+0.5])

plt.yticks([])
plt.xlabel("Time [s]", fontsize=f_size)
plt.ylabel("Spike Trains", fontsize=f_size)

letter_length = 0.003

for i in range(len(st_tr)):
    for j in range(10):
        start = j*letter_length
        stop = start + letter_length

        if len(st_tr[i].spiking_times[(st_tr[i].spiking_times > start) & (st_tr[i].spiking_times < stop)]) > 0:
            character = '1'
        else:
            character = '0'
        
        plt.text(0.003*j + 0.0015, i+1-0.3, character, horizontalalignment='center', verticalalignment='center', fontsize=14)
