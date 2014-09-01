import numpy as np
import matplotlib.pyplot as plt

class SpikeTrain():
    """
    Defines a SpikeTrain object.
    
    This object contains the raw spike times, as well as the
    methods to partition into words and letters. It will also 
    contain the time resolution for letters and words.
    
    NOTE: If data list is empty, spike train should still work,
    must fix!!!!!!
    """
    def __init__(self, data, start_time=None, end_time=None):
        """
        Initialises the SpikeTrain object from a list of 
        spike times.
        
        Care must be taken if spike trains are empty. In that case,
        it is necessary to create instances by specifying the start and 
        end time of the stimuli.
        """
        
        if len(data) == 0:
            self.empty = True # flag for spike trains with no spikes
        else:
            self.empty = False
        
        if start_time is None:
            if not self.empty:
                self.start_time = int(data[0])
            else:
                self.start_time = 0
        else:
            self.start_time = start_time
            
        if end_time is None:
            if not self.empty:
                self.end_time = int(data[-1] + 1.0)
            else:
                self.end_time = 1
        else:
            self.end_time = end_time       
        
        if len(data) == 0:
            self.empty = True # flag for spike trains with no spikes
        
        self.spiking_times = np.array(data)
        self.letters = None
        self.letter_width = None   #time resolution of letters
        self.words = None
        self.word_width = None     #time resolution of words
        self.letters_per_word = None
        self.t = None              #array of time to be used for kernel metric calculation#
        self.t_res = None
        
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
            if self.letter_width is not None:
                time_resolution = self.letter_width/2.0 # Sampling nyquist...
            else:
                time_resolution = min(self.spiking_times[1:] - self.spiking_times[:-1])/2.0
        
        self.t = np.arange(self.start_time, self.end_time + time_resolution, time_resolution)
        self.t_res = time_resolution  #time resoution for t array (just to have it explicitly)
        
    def make_hist(self):
        """
        Makes a histogram of the spiking times, for bins defined by the array
        self.t, by default it ensures that there is at most one count per bin.
        this histogram will be used to calculate the kernel metric.
        
        This function also compiles a list of indices for the spikes in the time array
        """
        h = np.histogram(self.spiking_times, self.t)
        self.hist = h
        self.arglist = np.argwhere(self.hist[0])
        self.arglist = self.arglist.flatten()
        
    def kernelise(self, kernel, bandwidth):
        """
        Returns an array where the kernels have been added for 
        the spiking times.
        
        kernel - kernel function that takes an array, a value and a bandwidth as arguments
        """
        
        self.make_hist()
        
        #arglist = np.argwhere(self.hist[0]) #arg list of nonzerom times
        #arglist = arglist.reshape(len(arglist),)
        
        self.kern_function = np.zeros(len(self.t))
        for i in self.arglist:
            #kernel(self.t - self.t[i], self.kern_function, bandwidth) #works for boxcar
            kernel(self.t, i, self.kern_function, bandwidth)
                    
    #def __repr__(self):
        #string = self.spiking_times.__repr__()
        #new_string = "SpikeTrain"+string[5:]
        #return new_string
        
    def shift_start_time(self, start=0, end=None):
        """
        Change the "absolute" value of the start time.
        Rewrites self.spiking_times and self.t (if it has been created)
        
        Use this method to make equivalent spike trains.
        """
        if end is None:
            end = self.end_time
        else:
            self.end_time = end
        
        self.spiking_times -= self.spiking_times[0] + start
        
        if self.t is not None:
            self.t = np.arange(start, self.end_time + self.t_res, self.t_res)
        
        
    def __getitem__(self, key):
        return self.spiking_times[key]
        
    def __len__(self):
        return len(self.spiking_times)
    
    def __str__(self):
        string = self.spiking_times.__repr__()
        new_string = "\t"+string[6:-1]
        return new_string


def boxcar(t, i, vals, bandwidth):
    """
    Boxcar/Uniform kernel
    
    Does not return anything, but updates the array passed
    as vals as many times as needed.
    """
    dt = t[1] - t[0]
    bins_in_band = int(bandwidth / dt)
    
    if bins_in_band <= 1:
        print "ERROR: Bandwidth must be higher"
        return
    
    if bins_in_band % 2 == 0:
        bins_in_band -= 1 #if number of bins is even, we reduce them by 1 (we are effectively rounding down...)
        
    lower = max(0, i - int(bins_in_band/2.0)) #dont go below index 0
    upper = i + int(bins_in_band/2.0)
    
    vals[lower:upper+1] += 1.0/bandwidth
    
def exp_kernel(t, i, vals, bandwidth):
    """
    Exponential kernel:
    (1/tau)exp(-t/tau), where tau is passed as the bandwidth
    
    Does not return anything, but updates the array passed as vals
    """
    tau = bandwidth
    vals[i:] += np.exp(-(t[i:] - t[i])/tau)/tau
    
    
def make_exp_kernel(spiking_times, tau):
    """
    Returns a function that will calculate the value of the kernel for the array passed
    
    tau - bandwidth of kernel
    """
    kernelised_function = lambda x: np.sum(np.array( [(1.0/tau)*new_neg_exp((x - i)/tau) for i in spiking_times] ), axis=0)
    return kernelised_function
    
def new_neg_exp(x):
    y = np.exp(-x)
    if isinstance(x, np.ndarray):
        y[y>1] = 0
    else:
        if y < 0:
            y = 0
    return y
        
#def distance(s1, s2):
    #dif = s1.kern_function - s2.kern_function
    #dif = dif**2
    #dif = sum(dif)/len(s1.t)
    #dif = np.sqrt(dif)
    
    #return dif
    
#def distance(s1, s2, tau=0.03):
    #"""
    #Calculates the distance between spike trains
    #using the analytic expression for the spike-train
    #metric.
    
    #Using this function, one can skip the kernelising 
    #stage all together, but the kernel bandwidth must still be
    #specified
    #"""
    
    #term1 = sum(np.array([[ np.exp(-abs(s1[i] - s1[j])/tau)  for i in range(len(s1))] for j in range(len(s1))]).flatten())
    #term2 = sum(np.array([[ np.exp(-abs(s2[i] - s2[j])/tau)  for i in range(len(s2))] for j in range(len(s2))]).flatten())
    #term3 = sum(np.array([[ np.exp(-abs(s1[i] - s2[j])/tau)  for i in range(len(s1))] for j in range(len(s2))]).flatten())
     
    #d = (term1 + term2 - 2*term3)/(2*tau)
     
    #return d
    
def distance(s1, s2, tau=0.03):
    """
    L2 distance between kernelised spike trains with the exponential kernel
    """

    term1 = np.array([[ -abs(s1[i] - s1[j])/tau  for i in range(len(s1))] for j in range(len(s1))]).flatten()
    term2 = np.array([[ -abs(s2[i] - s2[j])/tau  for i in range(len(s2))] for j in range(len(s2))]).flatten()
    term3 = np.array([[ -abs(s1[i] - s2[j])/tau  for i in range(len(s1))] for j in range(len(s2))]).flatten()
    
    term1 = np.exp(term1)
    term2 = np.exp(term2)
    term3 = np.exp(term3)
    
    d = (sum(term1) + sum(term2) -2*sum(term3))/(2*tau) 
    
    return d

    
def make_distance_matrix(spike_train_list, tau=0.03):
    """
    Makes a distance matrix for the responses given 
    in spike_train_list.
    """
    no_stim = len(spike_train_list)
    
    rows = [[distance(spike_train_list[j], spike_train_list[k], tau) 
             for k in range(j+1, no_stim)] for j in range(no_stim-1)]
    
    matrix = np.zeros(no_stim*no_stim).reshape(no_stim,no_stim)
    for i in range(no_stim-1):
        matrix[i,i+1:] = rows[i]

    matrix += matrix.T
    
    return matrix
    
def mi_from_dm(spike_train_list, distance_matrix, ns, nh):
    """
    Calculates the mutual information from the distance matrix and the responses
    (using the kernel density method) taking into account nh nearest neighbours
    
    responses should be a 1x(ns . nt) array of spike trains (a flattened array)
    """
    
    nearest_neighbours = np.array([r.argsort()[:nh] for r in distance_matrix])
    
    counts = []
    for i in range(len(nearest_neighbours)):
        c_i = 1
        for j in nearest_neighbours[i]:
            if (i != j and spike_train_list[i].start_time == spike_train_list[j].start_time):
                c_i += 1 
        counts.append(c_i)
    counts = np.array(counts)
    
    I = sum(np.log2(counts*ns/float(nh))) / float(len(spike_train_list))

    return I
    
def raster_plot(spike_train, y_pos=1):
    """
    Plots a raster_plot of a spike train.
    The y_pos is where the points will be aligned on the y axis.
    """
    spikes = spike_train.spiking_times
    spike_points = []
    for s in spikes:
        point = np.array([s, y_pos])
        spike_points.append(point)
    spike_points = np.array(spike_points)
    plt.plot(spike_points[:,0], spike_points[:,1], '.k')
    
def plot_trains_raster(spike_train_array):
    """
    Does a raster plot of many spike trains using the function 
    raster plot.
    """
    N = len(spike_train_array)
    
    for i in range(N):
        raster_plot(spike_train_array[i], i+1)
        plt.ylim([0, N+0.5])
    
    
    
    #smallest_diff = min(spikes[1:] - spikes[:-1])
    #t = np.arange(min(spikes), max(spikes) + smallest_diff ,smallest_diff)
    
#class DistMatrix():
    #def __init__(self, list_of_spike_trains):
        #self.ST = list_of_spike_trains

    #def __call__(self, i,j):
        #d = distance(self.ST[i], self.ST[j])
        #return d