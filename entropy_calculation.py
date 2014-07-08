#import numpy as np
from parsing import *


spike_times = np.loadtxt("Sfly01508SpikeTimes.txt")

repeated_exp = split_into_runs(spike_times, 5, 1000)

experiments_letters = [make_letters(i, int(i[0]), 5, 0.003) for i in repeated_exp]

experiments_words = [split_into_words(d, 10) for d in experiments_letters]

experiment_distributions = [word_distribution(e) for e in experiments_words]

time_distributions = word_distribution_given_time(experiments_words)

entropy_total = calculate_entropy(experiment_distributions[0])

entropies_t = [calculate_entropy(e) for e in time_distributions]