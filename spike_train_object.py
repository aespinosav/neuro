import numpy as np

class SpikeTrain():
    """
    Defines a SpikeTrain object.
    
    This object contains the raw spike times, as well as the
    methods to partition into words and letters. It will also 
    contain the time resolution for letters and words.
    """
    def __init__(self, data, start_time=None, end_time=None):
        """
        Initialises the SpikeTrain object from a list of 
        spike times.
        """
        if start_time is None:
            self.start_time = int(data[0])
        else:
            self.start_time = start_time
            
        if end_time is None:
            self.end_time = int(data[-1] + 1.0)
        else:
            self.end_time = end_time       
        
        self.spiking_times = np.array(data)
        self.letters = None
        self.letter_width = None   #time resolution of letters
        self.words = None
        self.word_width = None     #time resolution of words
        self.letters_per_word = None
        self.t = None              #array of time to be used for kernel metric calculation
        
    def make_letters(self, letter_interval, start_time=None, experiment_time=None):
        """
        Parses spike time data into letters.

        Each letter is made by temporally binning spiking data (either 1 or 0)
        letter_interval - the size of the bins (in seconds)
        start_time = start time (in seconds) of the experiment
        experiment_time - the length of the experiment (in seconds)
        
        By default the start_time and end_time of the object are used, unless otherwise
        specified.
        
        Returns a lsit of letter numpy arrays
        only bins that are fully contained within the experiment time are considered
        """
        if start_time is None:
            start_time = self.start_time
        
        if experiment_time is None:
            experiment_time = self.end_time - self.start_time
        
        number_of_letters = int(experiment_time / letter_interval)
        letter_array = np.zeros(number_of_letters).astype(int)

        spike_bins = (self.spiking_times - start_time)/letter_interval
        spike_bins = map(int, spike_bins)

        for i in spike_bins:
            letter_array[i] = 1

        self.letters = letter_array
        self.letter_width = letter_interval
        
    def make_words(self, word_length):
        """
        Makes a word array from letters

        word_length - number of letters in a word
        """
        number_of_words = int(len(self.letters) / float(word_length))
        
        word_list = []
        for i in range(number_of_words):
            current_word = ''
            for j in range(word_length):
                current_word += str(self.letters[i*word_length + j])

            word_list.append(current_word)

        self.words = word_list
        self.letters_per_word = word_length
        self.word_width = self.letters_per_word * self.letter_width
        
    
    def make_time_array(self, time_resolution=None):
        """
        Makes a time array on which kernel metrics will be calculated.
        
        By default, the resolution will be taken as the length of the time bin 
        for letters. However this can be specified.
        """
        if time_resolution is None:
            time_resolution = self.letter_width
        
        self.t = np.arange(self.start_time, self.end_time + time_resolution, time_resolution)
        
        
    #def __repr__(self):
        #string = self.spiking_times.__repr__()
        #new_string = "SpikeTrain"+string[5:]
        #return new_string
    
    def __str__(self):
        string = self.spiking_times.__repr__()
        new_string = "\t"+string[6:-1]
        return new_string