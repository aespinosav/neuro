"""
This file takes data from calculation
to see the sensitivity of the kde method
of calculating the mutual information and
plots the corresponding graph.

MI as the number of trials increases
different lines are used for different
number of stimuli.
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

ns_list = list(set([n for n in data[:,0]]))
ns_list.sort()

data_for_lines = np.array([[d for d in data if d[0]==ns] for ns in ns_list])

for ns in ns_list[-5:]:

    indx = ns_list.index(ns)
    label="$n_s =$ {}".format(int(ns))
    INFO = data_for_lines[indx,:,3]
    NT = data_for_lines[indx,:,1]
        
    plt.plot(NT, INFO, label=label)
    
plt.legend(loc='lower left', fancybox=True)
plt.xlabel("$n_t$")
plt.ylabel("Mutual Information [bits]")

plt.savefig("mi_vs_nt.pdf")