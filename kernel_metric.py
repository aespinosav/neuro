import numpy as np
import scipy as sp


#def boxcar(t, dt):
    #"""
    #Boxcar kernel
    #"""
    #t = np.array(t)
    #bound1 = t > -dt/2.0
    #bound2 = t < dt/2.0
    
    #non_zero = [all((bound1[i], bound2[i])) for i in range(len(t))]
    
    #vals = np.zeros(len(t))
    #vals[non_zero] = 1.0/dt
    
    #return vals
    
def boxcar(t, bandwidth):
    
    N = len(t)
    vals = np.zeros(N)
    
    for i in range(N):
        if t[i] > -dt/2.0 and t[i] < dt/2.0:
            vals[i] = 1.0/dt
            
    return vals
    
#def convolve(spike_letters, kernel)

def boxcar2(y, t, i, bandwidth):
    N = len(y)
    vals = np.zeros(N)
    
    for j in range(N):
        if t[i] > -dt/2.0 and t[i] < dt/2.0:
            vals[i] = 1.0/dt


def kernelise(self, kernel):
    """
    Returns an array where the kernels have been added for 
    the spiking times.
    
    kernel - kernel function that takes an array, a value and a bandwidth as arguments
    """
    
    
    arglist = np.argwhere(self.hist[0]) #arg list of nonzerom times
    
    y = np.zeros(len(self.t))
    for i in arglist:
        y += kernel(y, t, i, bandwidth)
        
    self.kern_function = y