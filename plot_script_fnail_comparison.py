data = np.loadtxt("data_meeting_conor.dat") #kde data
#data_discrete = np.loadtxt("discrete_data_matching_meeting.dat")

data_discrete = []
for n_trials in range(10,71,5):
    spike_times = np.loadtxt("./data/Sfly01508SpikeTimes.txt")
    repeated_exp = split_into_runs(spike_times, 200, 1000)
    repeated_exp_used = repeated_exp[:n_trials]
    repeated_exp_used = [repeated_exp_used[i] - 5*i for i in range(len(repeated_exp_used))]
    
    #Sort spikes into words
    responses_letters = [convert_to_letters(repeated_exp_used[i], letter_length, 0, 5) for i in range(len(repeated_exp_used))]
    responses_words = [convert_to_words(d, letters_per_word) for d in responses_letters]

    experiment_distributions = [word_distribution(e) for e in responses_words]
    time_distributions = word_distributions_given_t(responses_words)

    entropy_total = s_total
    entropies_noise = [calculate_entropy(e) for e in time_distributions]
    entropy_noise = np.average(entropies_noise)
    I_binning = entropy_total - entropy_noise

    data_discrete.append(I_binning)
    
data_discrete = np.array(data_discrete)


#data_discrete = data_discrete[data_discrete[:,0].argsort()]

plt.plot(data[:,2], data[:,-1], "o-k", label="KDE method")
plt.plot(data[:,2], data_discrete, "o-g", label="Discrete method")

plt.hlines(np.log2(166), 10, 70, linestyle="--")
plt.hlines(s_total, 10, 70, linestyle="--", color="g")

plt.grid(True)
plt.ylim([4, 7.5])
plt.xlim([10,70])
plt.legend(loc='lower left' )

plt.xlabel("$n_t$", fontsize=18)
plt.ylabel("$I(R;S)$ [bits]", fontsize=16)

