import numpy as np
from collections import Counter

def split_into_runs(spike_data, number_of_runs, total_length):
    """
    Splits the spiking data array into arrays for each run.

    spike_data - a numpy array
    length_of_run - time of individual experiment (in seconds)
    total_length - time of total data sample (in seconds)
    Returns an array of arrays (numpy).
    """
    length_of_run = total_length/float(number_of_runs)
    array_of_runs = []

    for i in range(number_of_runs):

        start = i*length_of_run
        stop = start + length_of_run

        run_data = spike_data[(start <= spike_data)&(spike_data <= stop)]

        array_of_runs.append(run_data)

    array_of_runs = [x for x in array_of_runs if len(x) != 0]

    print "{} runs were found".format(len(array_of_runs))


    return np.array(array_of_runs)


def split_into_stimuli(run, time_of_run, number_of_stim):
    """
    Splits a run into smaller sectiosn corresponding to
    an "individual" stimulus. As opposed to the split_into_runs
    function it will keep empty lists.

    This function assumes that all experiment time has been accounted for.

    run - np array of spike times
    time_of_run - length of run in seconds
    number_of_stim - number of stimuli to split run into
    """

    length_of_stim = float(time_of_run)/number_of_stim
    array_of_responses = []

    for i in range(number_of_stim):
        start = i*length_of_stim
        stop = start + length_of_stim

        stim_data = run[(start <= run)&(run <= stop)]

        array_of_responses.append(stim_data)
        array_of_runs = np.array(array_of_responses)

    return array_of_runs



def convert_to_letters(spike_data, letter_interval, start_time, experiment_time):
    """
    Parses spike time data into letters.

    Each letter is made by temporally binning spiking data (either 1 or 0)
    letter_interval - the size of the bins (in seconds)
    start__time = start time (in seconds) of the experiment
    experiment_time - the length of the experiment (in seconds)
    Returns a lsit of letter numpy arrays

    only bins that are fully contained within the experiment time are considered
    """
    number_of_letters = int(experiment_time / letter_interval)
    letter_array = np.zeros(number_of_letters).astype(int)

    spike_bins = (spike_data - start_time)/letter_interval
    spike_bins = map(int, spike_bins)

    for i in spike_bins:
        letter_array[i] = 1

    return letter_array



def convert_to_words(letter_exp, letters_per_word):
    """
    Splits data that has been converted into letters into words
    returns a list of words

    letter_exp - an array or list of letters for an experiment
    letters_per_word - number of letters in a word
    """

    number_of_words = int(len(letter_exp) / float(letters_per_word))

    word_list = []

    for i in range(number_of_words):
        current_word = ''
        for j in range(letters_per_word):
            current_word += str(letter_exp[i*letters_per_word + j])

        word_list.append(current_word)

    return word_list


    

def word_distribution(words):
    """
    Counts words and returns and rturns dict that has the word (string) as a key
    and the valued is the frecuency.

    words - dictionary of words (like the one that is returned by the split_into_words function)
    """

    distribution_dict = {}
    for w in words:
        if distribution_dict.has_key(w):
            distribution_dict[w] += 1
        else:
            distribution_dict[w] = 1

    return distribution_dict


def merge_distributions(dist_list):
    counters = map(Counter, dist_list)
    new_dist = np.sum(counters)
    
    return new_dist
    
    


def word_distributions_given_t(array_of_experiments):
    """
    Compiles a distribution dic for words given the time at which they happened.

    array_of_experiments - an array of the data converted into words.
    returns a distribution dictionary like the one returned by word_distribution.

    The experiments must have the same number of words!
    """
    distribution_array = []

    word_lists = [[d[i] for d in array_of_experiments]
                   for i in range(len(array_of_experiments[0]))]

    for l in word_lists:
        timestep_dict = {}

        for j in l:
            if timestep_dict.has_key(j):
                timestep_dict[j] += 1
            else:
                timestep_dict[j] = 1

        distribution_array.append(timestep_dict)

    return distribution_array
    

def number_of_words_observed(distribution_dict):
    """
    Returns the number of words observed from distribution_dict
    """
    return len(distribution_dict)
    


def calculate_entropy(distribution_dict):
    """
    Calculates entropy from distribution dictionary

    distribution_dict - Dictionary with keys for words / freq for values
    """

    total_words = sum(distribution_dict.values())
    P = [float(i)/total_words for i in distribution_dict.itervalues()]
    
    entropy = -sum(P*np.log2(P))

    return entropy

