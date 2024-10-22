# Monte Carlo integration
import numpy as np
import matplotlib.pyplot as plt

a = 0 # lower boundary
b = np.pi # upper boundary
N = 10000 # Number of iterations
areas =[]

for _ in range(N):
    answer = (b-a)/N * np.sin(np.random.uniform(a,b,N)).sum()
    areas.append(answer)

fig, ax = plt.subplots(figsize=(6,6))

ax.hist(areas, bins=31, ec='b')

mu = np.array(areas).mean()
sigma = np.array(areas).std()

textstr = f'$\mu=${mu:.2f}\n$\sigma=${sigma:.2f}'
props = dict(boxstyle='round', facecolor='blue', alpha=0.1)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.title("Distribution of calculated areas")
plt.xlabel("Area")
# plt.savefig('Monte_Carlo_integration.png')
plt.show()
