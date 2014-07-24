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
    
def boxcar(t, dt):
    
    N = len(t)
    vals = np.zeros(N)
    
    for i in range(N):
        if t[i] > -dt/2.0 and t[i] < dt/2.0:
            vals[i] = 1.0/dt
            
    return vals
    
#def convolve(spike_letters, kernel)