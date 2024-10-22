# Monte Carlo Pi Estimation
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from statistics import mean

ntimes = 5000
npoints = 10000
pi_estimation = []

for i in range(ntimes):
    x_rand = random.rand(npoints)  # Random x coordinate
    y_rand = random.rand(npoints)  # Random y coordinate
    inside = sum((x_rand-0.5)**2+(y_rand- 0.5)**2<0.25)
    pi_estimation.append(4*inside/npoints)

f, ax = plt.subplots(figsize=(6,6))
plt.title(f'Pi stimation.\nNº repetitions: {ntimes} | Nº points: {npoints}')

mu = mean(pi_estimation)
sigma = np.std(pi_estimation)
textstr = f'$\mu=${mu:.4f}\n$\sigma=${sigma:.4f}'
props = dict(boxstyle='round', facecolor='blue', alpha=0.1)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

ax.hist(pi_estimation, 30, ec='b')
ax.axvline(x=np.pi, color='r', linestyle='-')
# plt.savefig('pi_estimation_n_times.png')
plt.show()
