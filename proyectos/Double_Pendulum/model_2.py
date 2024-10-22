import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation, PillowWriter

def double_pendulum_model(y, t, L1, L2, m1, m2):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    theta1, z1, theta2, z2 = y

    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

    theta1dot = z1
    z1dot = (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
             (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2)
    theta2dot = z2
    z2dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + 
             m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
    return theta1dot, z1dot, theta2dot, z2dot

def get_xy(theta1, theta2):
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    return x1, y1, x2, y2

delta_t = 0.01
t = np.arange(0, 20, delta_t)

# Pendulum rod lengths (m), masses (kg).
L1, L2 = 1, 3.1
m1, m2 = 1, 1
# The gravitational acceleration (m.s-2).
g = 9.81
y0 = np.array([1.3, 0, 2.3, 0])

y = odeint(double_pendulum_model, y0, t, args=(L1, L2, m1, m2))

theta1, theta2 = y[:,0], y[:,2]
x1, y1, x2, y2 = get_xy(theta1, theta2)

fig, ax  = plt.subplots(figsize=(8,8),facecolor='.85')
# Plot the results
m1_trajectory, = ax.plot([], [], alpha=.3)
m2_trajectory, = ax.plot([], [], alpha=.3)
# ax.set_title('Dpubnle Pendulum')
line_m1_back, = ax.plot([0,x1[0]], [0,y1[0]], '-', color='k', lw=12, solid_capstyle='round')
line_m1_front, = ax.plot([0,x1[0]], [0,y1[0]], '-', color='w', lw=10, solid_capstyle='round', zorder=2)
m1_dot, = ax.plot(x1[0], y1[0], 'o', color='k', markersize=20, zorder=3)

line_m2_back, = ax.plot([x1[0],x2[0]], [y1[0],y2[0]], '-', color='k', lw=12, solid_capstyle='round')
line_m2_front, = ax.plot([x1[0],x2[0]], [y1[0],y2[0]], '-', color='w', lw=10, solid_capstyle='round', zorder=2)
m2_dot, = ax.plot(x2[0], y2[0], 'o', color='k', markersize=20, zorder=3)

ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-L1-L2,L1+L2)
ax.set_ylim(-L1-L2,L1+L2)

#############################

def animate(i):
    m1_trajectory.set_data(x1[:i], y1[:i])
    m2_trajectory.set_data(x2[:i], y2[:i])
    line_m1_back.set_data([0,x1[i]],[0,y1[i]])
    line_m1_front.set_data([0,x1[i]],[0,y1[i]])
    line_m2_back.set_data([x1[i],x2[i]],[y1[i],y2[i]])
    line_m2_front.set_data([x1[i],x2[i]],[y1[i],y2[i]])
    m1_dot.set_data(x1[i], y1[i])
    m2_dot.set_data(x2[i], y2[i])

fps = 25
every_x_frame = 1 / (delta_t*fps)
an = FuncAnimation(fig, animate, frames= np.arange(0,len(t),int(every_x_frame)), interval=20, repeat=False)
plt.show()


