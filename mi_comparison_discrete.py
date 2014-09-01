from parsing import *
from spike_train_object import *
"""
This script runs both the binning method and the kernel method for the 
same values of the stimulus length and word length.

Future versions of this script should probably increase the number of trials as well
to see how the mutual information values converge as the ammount of data is increased.

We will make the word lenghth as close to 30 ms as possible.
"""

#n_trials = 20
#n_stim = 
#t_stim = 5.0/n_stim
#word_length = round(t_stim/0.03)
#letters_per_word = 10
#letter_length = word_length/float(letters_per_word)


#n_trials = 5

trials_range = range(3,51)

n_stim = 166
t_stim = word_length = 5.0/n_stim
letters_per_word = 10
letter_length = float(word_length) / letters_per_word

#Arrays to store data 
NTrials = []
NStim = np.ones(len(trials_range))*n_stim
Nh = [] #number of neighbours used for the calculation
TStim = np.ones(len(trials_range))*t_stim #time duration of each stimulus
LPW = np.ones(len(trials_range))*letters_per_word #letters per word list
Stot = []
Snoise = []
Ibin = []
Ikern = []


for n_trials in trials_range:
    
    nh = n_trials

    #Import data and separate into individual experiment runs
    spike_times = np.loadtxt("./data/Sfly01508SpikeTimes.txt")
    repeated_exp = split_into_runs(spike_times, 200, 1000)
    repeated_exp_used = repeated_exp[:n_trials]
    repeated_exp_used = [repeated_exp_used[i] - 5*i for i in range(len(repeated_exp_used))]

    #create spikes from each run
    responses = np.array([split_into_stimuli(experiment, 5,  n_stim) for experiment in repeated_exp_used])
    responses_trains = np.array([[SpikeTrain(e[i], t_stim*i, t_stim*(1 + i)) for i in range(len(e))] for e in responses])
    responses_trains = responses_trains.flatten()
    #do the calculations for KDE
    DM = make_distance_matrix(responses_trains)
    I_kernel_method = mi_from_dm(responses_trains, DM, n_stim, nh)

    #Sort spikes into words
    responses_letters = [convert_to_letters(repeated_exp_used[i], letter_length, 0, 5) for i in range(len(repeated_exp_used))]
    responses_words = [convert_to_words(d, letters_per_word) for d in responses_letters]

    experiment_distributions = [word_distribution(e) for e in responses_words]
    time_distributions = word_distributions_given_t(responses_words)

    entropy_total = calculate_entropy(merge_distributions(experiment_distributions))
    entropies_noise = [calculate_entropy(e) for e in time_distributions]
    entropy_noise = np.average(entropies_noise)
    I_binning = entropy_total - entropy_noise
    
    
    NTrials.append(n_trials)
    Nh.append(nh) 

    Stot.append(entropy_total)
    Snoise.append(entropy_noise)
    Ibin.append(I_binning)
    
    Ikern.append(I_kernel_method)
    
data = np.column_stack((NTrials, NStim, Nh, TStim, LPW, Stot, Snoise, Ibin, Ikern))
np.savetxt("mutual_info_comparison.dat", data)