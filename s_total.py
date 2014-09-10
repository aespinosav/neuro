from parsing import *

spike_times = np.loadtxt("./data/Sfly01509SpikeTimes.txt")
run = split_into_runs(spike_times, 1, 990)
letters = convert_to_letters(run[0], 0.003, 0, 990)
words = convert_to_words(letters, 10)
dist = word_distribution(words)

s_total = calculate_entropy(dist)