import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity

def myround(x, prec=2, base=0.05):
    return round(base * round(float(x)/base), prec)

N = 30

X = np.concatenate((np.random.normal(-1, 1, 0.1*N),
                    np.random.normal(3, 1, 0.2*N),
                    np.random.normal(7, 2, 0.7*N)))[:, np.newaxis]
                    
X_plot = np.linspace(-5, 15, 1000)[:,None]
bins = np.linspace(-6, 20, 20)

true_density = (0.1* norm(-1, 1).pdf(X_plot[:,0]) 
                + 0.2* norm(3, 1).pdf(X_plot[:,0])
                + 0.7* norm(7, 2).pdf(X_plot[:,0]))

fig, ax = plt.subplots(2, 1, sharex=True)
#fig.subplots_adjust(hspace=0.05, wspace=0.05)

#Hist 1
hist1 = ax[0].hist(X[:,0], bins=bins, normed=True, fc='#bfaaff')
ax[0].plot(X_plot[:,0], true_density, "--k", linewidth=1.5)
ax[0].plot(X[:,0], np.zeros(len(X)), "or", markersize=5)
#plt.ylabel("Probability density")

#Hist 2
hist2 = ax[1].hist(X[:,0], bins=bins + 0.75, normed=True, fc='#bfaaff')
ax[1].plot(X_plot[:,0], true_density, "--k", linewidth=1.5)
ax[1].plot(X[:,0], np.zeros(len(X)), "or", markersize=5)


max_tick = max(np.concatenate((hist1[0],hist2[0])))
max_tick = myround(max_tick)

ax[0].set_yticks(np.arange(0,max_tick+0.05, 0.05))
ax[1].set_yticks(np.arange(0,max_tick+0.05, 0.05))

#ax[0].set_yticks(np.linspace(0, max_tick,5))
#ax[1].set_yticks(np.linspace(0, max_tick,5))   

#fig.ylabel("Probability density")
#ax[1].ylabel("Probability density")
ax[0].set_ylabel("Probability density", fontsize=14)
ax[1].set_ylabel("Probability density", fontsize=14)
fig.tight_layout()

plt.xlim([-5,15])


#######################################################
KDE estimation
#######################################################






N = 100

X = np.concatenate((np.random.normal(-1, 1, 0.1*N),
                    np.random.normal(3, 1, 0.2*N),
                    np.random.normal(7, 2, 0.7*N)))[:, np.newaxis]
                    
X_plot = np.linspace(-5, 15, 1000)[:,None]



fig2, ax2 = plt.subplots()

kernel = 'gaussian'


ax2.fill(X_plot[:,0], true_density, fc='black', alpha=0.3, label='True distribution')

bw_range = [0.3, 0.5, 1.5]

for bandwidth in  bw_range:
    kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(X)
    log_dens = kde.score_samples(X_plot)
    ax2.plot(X_plot[:,0], np.exp(log_dens), '-', label='Bandwidth = {}'.format(bandwidth))

ax2.plot(X[:,0], np.zeros(len(X)), "or", markersize=5)
    
ax2.legend(loc='upper left')
ax2.set_ylabel('Probability density')
ax2.text(6, 0.38, "N={0} points".format(N))
fig2.tight_layout()