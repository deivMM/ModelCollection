import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Constants
G = 9.81  # gravitational constant
L1 = 1.0  # length of pendulum 1
L2 = 1.0  # length of pendulum 2
M1 = 1.0  # mass of pendulum 1
M2 = 1.0  # mass of pendulum 2

def double_pendulum(state, t):
    """Compute the derivatives of the state vector."""
    theta1, omega1, theta2, omega2 = state
    
    # Precompute some constants
    c1 = np.cos(theta1)
    s1 = np.sin(theta1)
    c2 = np.cos(theta2)
    s2 = np.sin(theta2)
    c12 = np.cos(theta1 - theta2)
    s12 = np.sin(theta1 - theta2)
    m12 = M1 + M2
    
    # Compute the derivatives
    dtheta1_dt = omega1
    domega1_dt = (M2*G*s2*c12 - m12*G*s1 - M2*L1*s12*omega1**2*s2 - M2*L2*omega2**2*s12*s2*c12) / (m12*L1 - M2*L1*c12**2)
    dtheta2_dt = omega2
    domega2_dt = ((m12*(G*s1*c12 - L1*omega1**2*s12 - G*s2) + M2*L2*omega2**2*s12) * c12) / (m12*L2 - M2*L2*c12**2)
    
    return [dtheta1_dt, domega1_dt, dtheta2_dt, domega2_dt]

# Initial conditions
state0 = [np.pi/2, 0, np.pi/2, 0]  # theta1, omega1, theta2, omega2
t = np.linspace(0, 10, 1000)  # time grid

# Solve the ODE system
states = odeint(double_pendulum, state0, t)

# Plot the results
theta1, omega1, theta2, omega2 = states.T
x1 = L1 * np.sin(theta1)
y1 = -L1 * np.cos(theta1)
x2 = x1 + L2 * np.sin(theta2)
y2 = y1 - L2 * np.cos(theta2)

fig, ax = plt.subplots()
ax.plot(x1, y1, 'b', label='Pendulum 1')
ax.plot(x2, y2, 'g', label='Pendulum 2')
ax.set_aspect('equal', 'datalim')
ax.legend()
plt.show()
