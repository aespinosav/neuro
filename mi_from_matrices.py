"""
Script to calculate the mutual information between 
spike train responses and stimuli using KDE method 
by Tobin & Houghton. It does so for previously
calculated distance matrices.

We are testing two variations to see if there really
is a difference or not.

The bandwidth of the kenrel is being indirectly 
determined by the number of neighbours we are using (nh).

This nh is choses as the number of trials (nt) as it is 
a natural choice (at least for the data we have at hand)
"""

from spike_train_object import *
import os
import re
from sys import argv


#We must make sure the directory contains only
#the files we want (distance matrices)




#directory = "./data/dist_matrices"
directory  = argv[1] #get directory of data 
directory_to_save = argv[2] #directory to save file to

data_file_name = "mutual_info_kde_final_final.dat"
data_file_name = directory_to_save + "/" + data_file_name

files_list = os.listdir(directory) #this directory must exis, of course...

NS = []
NT = []
I_C = []
I_A = []
I_MAX = []

print "Will process {} distance matrices... \n".format(len(files_list))

counter = 0

for f_name in files_list:
    counter += 1
    print "Processing matrix {}:\n".format(counter)+f_name+"...\n"
    
    path = directory+'/'+f_name
    
    seq = filter(None, re.split("[_.]", f_name))
    ns = int(seq[seq.index('ns') + 1])
    nt = int(seq[seq.index('nt') + 1])
   
    nr = ns*nt
    

    dm = np.loadtxt(path)
    #dm = np.sqrt(dm) #once new matrix files are used this line should be removed
    
    I_conor = mi_from_dm(dm, ns, nt)
    I_alonso = mi_from_dm_alt(dm, ns, nt)
    I_max = np.log2(ns)
    
    NS.append(ns)
    NT.append(nt)
    I_C.append(I_conor)
    I_A.append(I_alonso)
    I_MAX.append(I_max)
    
data = np.column_stack((NS, NT, I_MAX, I_C, I_A))
fmt = '%d\t%d\t%f\t%f\t%f'

header = '#n_s\tn_t\tmax_information\tinformation_conor\tinformation_alonso\n'

with open(data_file_name, 'w') as f:
    f.write(header)
    np.savetxt(f, data, fmt=fmt)

#NOTE this data file is not ordered
#it needs processing and sorting to get good graphs