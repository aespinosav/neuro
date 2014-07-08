import numpy as np

#split data into individual runs (5 sec chunks)
#experiment_runs = [[] for i in range(20)]

def split_into_runs(spike_data, length_of_run, total_length):
    """
    Splits the spiking data array into arrays for each run.

    spike_data - a numpy array
    length_of_run - time of individual experiment (in seconds)
    total_length - time of total data sample (in seconds)
    Returns an array of arrays (numpy).
    """

    experiment_runs = [spike_data[(start <= spike_data) & (spike_data <= start + length_of_run)] - start
                       for start in range(0, total_length + length_of_run, length_of_run) ]

    return np.array(experiment_runs)



def make_letters(spike_times, start_time,  length_of_data, letter_interval=0.003):
    """
    Parses spike time data into letters.

    Each letter is made by temporally binning spiking data (either 1 or 0)
    letter_interval - the size of the bins (in seconds)
    length_of_data - the length of the experiment (in seconds)

    Returns a dictionary  {bin number : state}
    """


    number_of_bins = int(length_of_data/letter_interval)

    bins = {i:0 for i in range(number_of_bins)}

    data = set(map(int, (spike_times - start_time)/letter_interval))
    data = list(data)

    for i in data:
        bins[i] = 1

    return bins


def split_into_words(data_dictionary, word_length):
    """
    Splits data that has been converted into letters into words
    returns dictionary with words

    data_dictionary - dict of bin:letter
    word_length - number of letters in a word
    """

    word_dict = {}
    current_key = 0
    current_word = ""
    
    for i in data_dictionary.iterkeys():
        
        if i>0 and i%word_length == 0:
            
            word_dict[current_key] = current_word
            #print current_word
            
            current_key += 1
            current_word = ""


        current_word += str(data_dictionary[i])

    return word_dict
    

def word_distribution(word_dict):
    """
    Counts words. Returns dict that has the word (string) as a key
    and the valued is the frecuency.

    word_dict - dictionary of words (like the one that is returned by the split_into_words function)
    """

    distribution_dict = {}
    for i in word_dict.itervalues():
        if distribution_dict.has_key(i):
            distribution_dict[i] += 1
        else:
            distribution_dict[i] = 1

    return distribution_dict

    
def word_distribution_given_time(array_of_experiments):
    """
    Compiles a distribution dic for words given the time at which they happened (word for word)

    array_of_experiments - an array of the data converted into words.
    returns a distribution dictionary like the one returned by word_distribution.
    """

    distribution_array = []

    word_lists = [[d[i] for d in array_of_experiments] for i in array_of_experiments[0].iterkeys()]

    for l in word_lists:
        timestep_dict = {}

        for j in l:
            if timestep_dict.has_key(j):
                timestep_dict[j] += 1
            else:
                timestep_dict[j] = 1

        distribution_array.append(timestep_dict)
    
    #for i in array_of_experiments[0].iterkeys():
        
        #timestep_dict = {}
        #word_list = [d[i] for d in array_of_experiments]
        
        #for j in word_list:
            #if timestep_dict.has_key(j):
                #timestep_dict[j] += 1
            #else:
                #timestep_dict[j] = 1
                
        #distribution_array.append(timestep_dict)

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

    total_words = number_of_words_observed(distribution_dict)
    P = [float(i)/total_words for i in distribution_dict.itervalues()]
    
    entropy = -sum(P*np.log2(P))

    return entropy



#Make letters from the spiking times
#bins = np.arange(0.003, 1000.1, 0.003)
#number_of_bins = len(bins)
#bins = {i:0 for i in range(number_of_bins)}

#data = set(map(int, spike_times/0.003))
#data = list(data)

#for i in data:
    #bins[i] = 1








#Make words out of each stimulus run