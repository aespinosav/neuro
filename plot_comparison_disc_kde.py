data = np.loadtxt("data_meeting_conor.dat") #kde data
data_discrete = np.loadtxt("discrete_data_matching_meeting.dat")
data_discrete = data_discrete[data_discrete[:,0].argsort()]

plt.plot(data[:,2], data[:,-1], "o-k", label="KDE method")
plt.plot(data_discrete[:,0], data_discrete[:,-1], "o-g", label="Discrete method")

plt.hlines(np.log2(166), 10, 70, linestyle="--")
plt.hlines(s_total, 10, 70, linestyle="--", color="g")

plt.grid(True)
plt.ylim([4, 7.5])
plt.legend(loc='lower left' )

plt.xlabel("$n_t$", fontsize=18)
plt.ylabel("$I(R,S)$ [bits]", fontsize=18)
