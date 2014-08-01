#import numpy as np
from parsing import *

spike_times = np.loadtxt("Sfly01508SpikeTimes.txt")
repeated_exp = split_into_runs(spike_times, 200, 1000)

experiments_letters = [convert_to_letters(i, 0.003, int(i[0]), 5) for i in repeated_exp]

experiments_words = [convert_to_words(d, 10) for d in experiments_letters]

experiment_distributions = [word_distribution(e) for e in experiments_words]

time_distributions = word_distributions_given_t(experiments_words)

entropy_total = calculate_entropy(experiment_distributions[0])

entropies_t = [calculate_entropy(e) for e in time_distributions]