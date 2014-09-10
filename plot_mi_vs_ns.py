"""
This file takes data from calculation
to see the sensitivity of the kde method
of calculating the mutual information and
plots the corresponding graph.

MI as the number of trials stimuli
different lines are used for different
number of trials.
"""

from spike_train_object import *
from parsing import *
from sys import argv

import matplotlib.pyplot as plt

data_file_name = argv[1]

data = np.loadtxt(data_file_name)

#The columns of the data correspond to 
##ns nt  max_information information_conor information_alonso

#First we sort the data by nt

data = data[data[:,1].argsort()]

nt_list = list(set([n for n in data[:,1]]))
nt_list.sort()

data_for_lines = np.array([[d for d in data if d[1]==nt] for nt in nt_list])
data_for_lines = np.array([ d[d[:,0].argsort()] for d in data_for_lines])

for nt in nt_list[-20:]:

    indx = nt_list.index(nt)
    label="$n_t =$ {}".format(int(nt))
    INFO = data_for_lines[indx,:,3]/data_for_lines[indx,:,2]
    NS = data_for_lines[indx,:,0]
        
    plt.plot(NS, INFO, label=label)
    
#plt.legend(loc='lower left', fancybox=True)
plt.xlabel("$n_s$")
plt.ylabel("$I(R;S)/I(S)")

plt.savefig("mi_vs_ns.pdf")
