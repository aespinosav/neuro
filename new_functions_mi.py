from parsing import *
from spike_train_object import *
import numpy as np

def mi_from_dm(distance_matrix, ns, nh, spike_train_list=None):
    """
    Calculates the mutual information from the distance matrix and the responses
    (using the kernel density method) taking into account nh nearest neighbours
    
    responses should be a 1x(ns . nt) array of spike trains (a flattened array)
    If None is passed then it is assumed that the distance matrix is given in an
    ordered way: r(trial_1)  r(trial_2) ...
    """
    
    nr = len(distance_matrix)
    nt = nr/ns
    nearest_neighbours = np.array([r.argsort()[:nh] for r in distance_matrix])
    
    if spike_train_list is not None:

        members_of_glob = trains_in_glob(spike_train_list)
        glob_comp = glob_composition(spike_train_list, ns, nt, nh)

        counts = []
        for i in range(len(nearest_neighbours)):
            c_i = 0
            
            if i not in members_of_glob:
                for j in nearest_neighbours[i]:
                    if j not in members_of_glob:
                        if spike_train_list[i].start_time == spike_train_list[j].start_time:
                            c_i += 1 # count neigbours out of glob
                        else:
                            f_i = glob_comp[i]/float(sum(glob_comp.values()))
                            c_i += (nh - c_i)*f_i # if one neighbour is in glob, all following neighb are as well
                            break
                counts.append(c_i)
            else:
                f_i = glob_comp[i]/float(sum(glob_comp.values()))
                c_i += 1 + (nh - 1)*f_i #If in glob, take fraction of remaining neighbours except you
                counts.append(c_i)
                        
        counts = np.array(counts)
     
    else:
        
        counts = []
        for i in range(len(nearest_neighbours)):
            c_i = 1
            for j in nearest_neighbours[i]:
                if (i != j and abs(i - j)%ns==0 ):
                    c_i += 1 
            counts.append(c_i)
        counts = np.array(counts)        
        
    I = sum(np.log2(counts*ns/float(nh))) / float(nr)

    return I
       
    
    
    
    
    
def mi_from_dm_alt(distance_matrix, ns, nh, spike_train_list=None):
    """
    Calculates the mutual information from the distance matrix and the responses
    (using the kernel density method) taking into account nh nearest neighbours.
    
    the way I think it should be working, because there might be a mistake in the 
    other method.
    """
    
    #print "start loading"
    
    nr = len(distance_matrix)
    nt = nr/ns
    nearest_neighbours = np.array([r.argsort()[:nh] for r in distance_matrix])
    near_to = [[j for j in range(nr) if i in nearest_neighbours[j] ] for i in range(nr)]
    
    #print "finished sorting"
    #return
    #nr = len(distance_matrix)
    #nearest_neighbours = np.array([[i] + distance_matrix[i].argsort()[1:nh].tolist() for i in range(nr)])
    
    members_of_glob = trains_in_glob(spike_train_list)
    glob_comp = glob_composition(spike_train_list, ns, nt, nh)
    
    counts = []
    counted_glob = False #set a flag for later use
    if spike_train_list is not None:
        for i in range(len(near_to)):
            c_i = 0
                  
            if i not in members_of_glob:
                #print near_to[i]
                for j in near_to[i]:
                    
                    if j not in members_of_glob and spike_train_list[i].start_time == spike_train_list[j].start_time:
                        c_i += 1
                    else:
                        if not counted_glob: #this should only really happen if glob has a small number of members...
                            f_i = glob_comp[i]/float(sum(glob_comp.values()))
                            g_i = f_i - 1.0/float(sum(glob_comp.values()))
                            c_i += (nh - c_i)*g_i
                            
                            counted_glob = True
                        else:
                            pass
                            
            else: #If i is in the glob...
                f_i = glob_comp[i]/float(sum(glob_comp.values()))
                g_i = f_i - 1.0/float(sum(glob_comp.values()))
                c_i = 1 + (nh - 1)*g_i
                
            counts.append(c_i)       
        counts = np.array(counts)        
        I = (1.0/nr)*sum( np.log2((ns*counts)/float(nh)) ) 
    
    else:
        near_to_same_stim = [[n for n in near_to[j] if abs(n-j)%ns==0 ] for j in range(nr)]
        number_of_neighbourhoods = np.array([len(l) for l in near_to])
        number_of_neighbourhoods_same_stim = np.array([len(l) for l in near_to_same_stim])
        I = (1.0/nr)*sum( np.log2((ns*number_of_neighbourhoods_same_stim)/float(nh)) )
    
    return I
    
    
    





def mi_from_dm_alt_hq(distance_matrix, ns, nh, spike_train_list=None):
    """
    Calculates the mutual information from the distance matrix and the responses
    (using the kernel density method) taking into account nh nearest neighbours.
    
    the way I think it should be working, because there might be a mistake in the 
    other method.
    """
    
    print "start loading"
    
    nr = len(distance_matrix)
    nt = nr/ns
    #nearest_neighbours = np.array([r.argsort()[:nh] for r in distance_matrix])
    nearest_neighbours = np.array([np.array(hq.nsmallest(nh, r)) for r in distance_matrix])
    near_to = [[j for j in range(nr) if i in nearest_neighbours[j] ] for i in range(nr)]
    
    print "finished sorting"
    return
    #nr = len(distance_matrix)
    #nearest_neighbours = np.array([[i] + distance_matrix[i].argsort()[1:nh].tolist() for i in range(nr)])
    
    members_of_glob = trains_in_glob(spike_train_list)
    glob_comp = glob_composition(spike_train_list, ns, nt, nh)
    
    counts = []
    counted_glob = False #set a flag for later use
    if spike_train_list is not None:
        for i in range(len(near_to)):
            c_i = 0
                  
            if i not in members_of_glob:
                #print near_to[i]
                for j in near_to[i]:
                    if j not in members_of_glob and spike_train_list[i].start_time == spike_train_list[j].start_time:
                        c_i += 1
                    else:
                        if not counted_glob: #this should only really happen if glob has a small number of members...
                            f_i = glob_comp[i]/float(sum(glob_comp.values()))
                            g_i = f_i - 1.0/float(sum(glob_comp.values()))
                            c_i += (nh - c_i)*g_i
                            
                            counted_glob = True
                        else:
                            pass
                            
            else: #If i is in the glob...
                f_i = glob_comp[i]/float(sum(glob_comp.values()))
                g_i = f_i - 1.0/float(sum(glob_comp.values()))
                c_i = 1 + (nh - 1)*g_i
                
            counts.append(c_i)       
        counts = np.array(counts)        
        I = (1.0/nr)*sum( np.log2((ns*counts)/float(nh)) ) 
    
    else:
        near_to_same_stim = [[n for n in near_to[j] if abs(n-j)%ns==0 ] for j in range(nr)]
        number_of_neighbourhoods = np.array([len(l) for l in near_to])
        number_of_neighbourhoods_same_stim = np.array([len(l) for l in near_to_same_stim])
        I = (1.0/nr)*sum( np.log2((ns*number_of_neighbourhoods_same_stim)/float(nh)) )
    
    return I