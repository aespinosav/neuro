def load_spike_trains(directory, ns, nt):
    
    spike_times = np.loadtxt(directory + "Sfly01508SpikeTimes.txt")
    repeated_exp = split_into_runs(spike_times, 200, 1000)
    repeated_exp_used = repeated_exp[:nt]
    spike_trains = [repeated_exp_used[i] - 5*i for i in range(len(repeated_exp_used))]
    
    t_stim = 5.0/ns
    
    responses = np.array([split_into_stimuli(experiment, 5,  ns) for experiment in spike_trains])
    responses_trains = np.array([[SpikeTrain(e[i], t_stim*i, t_stim*(1 + i)) for i in range(len(e))] for e in responses])
    
    
    return responses_trains
t_stim = 5.0/166.0
t_letter = t_stim/10.0
entropy_total = s_total

repeated_exp_used = load_spike_trains("./data/", 166, 198)

responses_letters = [convert_to_letters(repeated_exp_used[i], t_letter, 0, 5.0) for i in range(len(repeated_exp_used))]
responses_words = [convert_to_words(d, 10) for d in responses_letters]

experiment_distributions = [word_distribution(e) for e in responses_words]
time_distributions = word_distributions_given_t(responses_words)

#entropy_total = calculate_entropy(merge_distributions(experiment_distributions))
entropies_noise = [calculate_entropy(e) for e in time_distributions]
entropy_noise = np.average(entropies_noise)
I_binning = entropy_total - entropy_noise
