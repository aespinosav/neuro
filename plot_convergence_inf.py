import matplotlib.pyplot as plt
import numpy as np

s_total = 7.0970062207842268
n_stim = 166

I_max = np.log2(n_stim)

data = np.loadtxt("mutual_info_comparison.dat")

Ntrials = data[:,0]

Snoise = data[:,-3]

I_bin = s_total - Snoise
I_kern = data[:,-1]

plt.plot(Ntrials, I_bin, label="Binning method")
plt.plot(Ntrials, I_kern, label="Kernel method")
plt.hlines(I_max,0, 60, linestyle="--")


plt.xlabel("$n_t$")
plt.ylabel("$I(R;S)$")
plt.grid(True)
plt.legend(loc="lower left")
plt.xlim([10,60])
plt.ylim([4,8])

plt.savefig("converging_I.pdf")


