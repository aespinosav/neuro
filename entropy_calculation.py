#import numpy as np
from parsing import *

spike_times = np.loadtxt("./data/Sfly01508SpikeTimes.txt")
repeated_exp = split_into_runs(spike_times, 200, 1000)

w_interval = (5.0/166)
l_interval = w_interval/10.0

experiments_letters = [convert_to_letters(i, l_interval, int(i[0]), 5) for i in repeated_exp]

experiments_words = [convert_to_words(d, 10) for d in experiments_letters]

experiment_distributions = [word_distribution(e) for e in experiments_words]

time_distributions = word_distributions_given_t(experiments_words)

#entropy_total = calculate_entropy(experiment_distributions[0])

entropies_t = [calculate_entropy(e) for e in time_distributions]
s_noise = np.mean(entropies_t)
entropy_total = s_total

I_bin = s_total - s_noise
print "I_bin = ", I_bin