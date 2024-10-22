import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp

def logistic_growth(N, t, r, K):
    """
    Calculates the rate of change of the population size using the logistic growth model.

    Parameters:
    N (float): population size
    t (float): time
    r (float): growth rate
    K (float): capacity

    Returns:
    dNdt (float): rate of change of population size
    """
    dNdt = r * N * (1 - N/K)
    return dNdt

P_range = np.linspace(0, 100, 50)
t_range = np.linspace(0.1, 100, 50) # time points

T, P = np.meshgrid(t_range, P_range)

p_0s = [1, 5, 10, 15, 20] # initial populations size
r_values = [0.05, 0.075, 0.1, 0.15, 0.2] # different growth rates to try
K = 100

for n, r in enumerate(r_values): 
    f, ax = plt.subplots(figsize=(10,10),facecolor='.85')

    dt = np.ones(P.shape)
    dp = logistic_growth(P, T, r, K)   
    pp = 0.5
    nn = (dt**2 + dp**2)**(pp)
    ax.quiver(T, P, dt/nn, dp/nn, angles='xy', alpha=0.5)
    
    for p_0 in p_0s:
        ax.plot(t_range, odeint(logistic_growth, p_0, t_range, args=(r,K)), 'b')
    ax.set_xlabel('time', fontsize=15)
    ax.set_ylabel('Population size', fontsize=15)
    plt.title(f'Growth rate: {r}', fontsize=15)
    plt.savefig(f'Image_{n+1}.png',facecolor='.85')
    plt.show()
