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

def get_xy(theta1, theta2, L1, L2):
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    return x1, y1, x2, y2

animate_TF = True  # Set to False to just plot the trajectory

tmax = 20 # max time
delta_t = 0.01
t = np.arange(0, tmax, delta_t)
g = 9.81 # The gravitational acceleration (m.s-2).

################################################
# Pendulum rod lengths (m), masses (kg), position [degrees] and velocity [degrees/sec]
L1, L2 = 3, 2
m1, m2 = 2, 3
m1_pos_degrees, m2_pos_degrees = 90, -180
m1_vel, m2_vel = 45, -20

y0 = np.array([np.radians(m1_pos_degrees), np.radians(m1_vel), np.radians(m2_pos_degrees), np.radians(m2_vel)])
y = odeint(double_pendulum_model, y0, t, args=(L1, L2, m1, m2))

theta1, theta2 = y[:,0], y[:,2]
x1, y1, x2, y2 = get_xy(theta1, theta2, L1, L2)

################################################

fig, (ax1, ax2)  = plt.subplots(1, 2, figsize=(12,6),facecolor='.85')
fig.suptitle('Double pendulum',fontsize=25,x=0.5,y=.96,weight='semibold')
# Plot the results
m2_trajectory, = ax1.plot([], [], alpha=.4, color='skyblue', lw=2)
line_m1_back, = ax1.plot([0,x1[0]], [0,y1[0]], '-', color='k', lw=4, solid_capstyle='round')
line_m1_front, = ax1.plot([0,x1[0]], [0,y1[0]], '-', color='w', lw=2, solid_capstyle='round', zorder=2)
m1_dot, = ax1.plot(x1[0], y1[0], 'o', markeredgecolor='black', markeredgewidth=1, color='skyblue', markersize=m1*6, zorder=3)

line_m2_back, = ax1.plot([x1[0],x2[0]], [y1[0],y2[0]], '-', color='k', lw=4, solid_capstyle='round')
line_m2_front, = ax1.plot([x1[0],x2[0]], [y1[0],y2[0]], '-', color='w', lw=2, solid_capstyle='round', zorder=2)
m2_dot, = ax1.plot(x2[0], y2[0], 'o', markeredgecolor='black', markeredgewidth=1, color='skyblue', markersize=m2*6, zorder=3)

ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_xlim((-L1-L2)*1.1,(L1+L2)*1.1)
ax1.set_ylim((-L1-L2)*1.1,(L1+L2)*1.1)

theta1_theta2_line, = ax2.plot([], [], alpha=.7, color='skyblue', lw=2)
theta1_theta2_dot, = ax2.plot([], [], 'o', markeredgecolor='black', markeredgewidth=1, color='skyblue', markersize=8)

ax2.axhline(0, color='k', lw=1, alpha=.2)
ax2.axvline(0, color='k', lw=1, alpha=.2)
ax2.set_xlabel(r'$\theta_1$ (rad)', fontsize=15)
ax2.set_ylabel(r'$\theta_2$ (rad)', fontsize=15)    

ax2.set_xlim(theta1.min()*1.1, theta1.max()*1.1)
ax2.set_ylim(theta2.min()*1.1, theta2.max()*1.1)

def animate(i):
    m2_trajectory.set_data(x2[:i], y2[:i])
    line_m1_back.set_data([0,x1[i]],[0,y1[i]])
    line_m1_front.set_data([0,x1[i]],[0,y1[i]])
    line_m2_back.set_data([x1[i],x2[i]],[y1[i],y2[i]])
    line_m2_front.set_data([x1[i],x2[i]],[y1[i],y2[i]])
    m1_dot.set_data([x1[i]], [y1[i]])
    m2_dot.set_data([x2[i]], [y2[i]])
    
    theta1_theta2_line.set_data([theta1[:i]], [theta2[:i]])
    theta1_theta2_dot.set_data([theta1[i]], [theta2[i]])

if animate_TF:
    fps = 25
    every_x_frame = 1 / (delta_t*fps)
    an = FuncAnimation(fig, animate, frames= np.arange(0,len(t),int(every_x_frame)), interval=20, repeat=False)
    plt.show()
else:
    m2_trajectory.set_data(x2, y2)
    line_m1_back.set_data([0,x1[-1]],[0,y1[-1]])
    line_m1_front.set_data([0,x1[-1]],[0,y1[-1]])
    line_m2_back.set_data([x1[-1],x2[-1]],[y1[-1],y2[-1]])
    line_m2_front.set_data([x1[-1],x2[-1]],[y1[-1],y2[-1]])
    m1_dot.set_data([x1[-1]], [y1[-1]])
    m2_dot.set_data([x2[-1]], [y2[-1]])
    
    theta1_theta2_line.set_data([theta1], [theta2])
    theta1_theta2_dot.set_data([theta1[-1]], [theta2[-1]])
    plt.show()
    