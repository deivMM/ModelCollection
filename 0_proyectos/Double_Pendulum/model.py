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

tmax = 20 # max time
delta_t = 0.01
t = np.arange(0, tmax, delta_t)
g = 9.81 # The gravitational acceleration (m.s-2).

################################################
# First pendulum 
################################################

# Pendulum rod lengths (m), masses (kg).
L1_p1, L2_p1 = 3, 2
m1_p1, m2_p1 = 1.5, 2

# m1_position and velocity
m1_pos_p1_degrees = 0
m1_vel_p1 = 5
# m2_position and velocity
m2_pos_p1_degrees = 0
m2_vel_p1 = -3

y0_p1 = np.array([np.radians(m1_pos_p1_degrees), m1_vel_p1, np.radians(m2_pos_p1_degrees), m2_vel_p1])
y_p1 = odeint(double_pendulum_model, y0_p1, t, args=(L1_p1, L2_p1, m1_p1, m2_p1))

theta1_p1, theta2_p1 = y_p1[:,0], y_p1[:,2]
x1_p1, y1_p1, x2_p1, y2_p1 = get_xy(theta1_p1, theta2_p1, L1_p1, L2_p1)

fig, ax  = plt.subplots(figsize=(8,8),facecolor='.85')
fig.suptitle('Double pendulum',fontsize=25,x=0.5,y=.94,weight='semibold')
# Plot the results
m2_p1_trajectory, = ax.plot([], [], alpha=.4, color='skyblue', lw=3)
line_m1_p1_back, = ax.plot([0,x1_p1[0]], [0,y1_p1[0]], '-', color='k', lw=4, solid_capstyle='round')
line_m1_p1_front, = ax.plot([0,x1_p1[0]], [0,y1_p1[0]], '-', color='w', lw=2, solid_capstyle='round', zorder=2)
m1_p1_dot, = ax.plot(x1_p1[0], y1_p1[0], 'o', markeredgecolor='black', markeredgewidth=1, color='skyblue', markersize=m1_p1*10, zorder=3)

line_m2_p1_back, = ax.plot([x1_p1[0],x2_p1[0]], [y1_p1[0],y2_p1[0]], '-', color='k', lw=4, solid_capstyle='round')
line_m2_p1_front, = ax.plot([x1_p1[0],x2_p1[0]], [y1_p1[0],y2_p1[0]], '-', color='w', lw=2, solid_capstyle='round', zorder=2)
m2_p1_dot, = ax.plot(x2_p1[0], y2_p1[0], 'o', markeredgecolor='black', markeredgewidth=1, color='skyblue', markersize=m2_p1*10, zorder=3)

################################################
# Second pendulum 
################################################
# Pendulum rod lengths (m), masses (kg).
L1_p2, L2_p2 = 3, 2
m1_p2, m2_p2 = 1.6, 2

# m1_position and velocity
m1_pos_p2_degrees = 0
m1_vel_p2 = 5
# m2_position and velocity
m2_pos_p2_degrees = 0
m2_vel_p2 = -3

y0_p2 = np.array([np.radians(m1_pos_p2_degrees), m1_vel_p2, np.radians(m2_pos_p2_degrees), m2_vel_p2])

y_p2 = odeint(double_pendulum_model, y0_p2, t, args=(L1_p2, L2_p2, m1_p2, m2_p2))

theta1_p2, theta2_p2 = y_p2[:,0], y_p2[:,2]
x1_p2, y1_p2, x2_p2, y2_p2 = get_xy(theta1_p2, theta2_p2, L1_p2, L2_p2)

# Plot the results

m2_p2_trajectory, = ax.plot([], [], alpha=.4, color='salmon', lw=3)
line_m1_p2_back, = ax.plot([0,x1_p2[0]], [0,y1_p2[0]], '-', color='k', lw=4, solid_capstyle='round')
line_m1_p2_front, = ax.plot([0,x1_p2[0]], [0,y1_p2[0]], '-', color='w', lw=2, solid_capstyle='round', zorder=2)
m1_p2_dot, = ax.plot(x1_p2[0], y1_p2[0], 'o', markeredgecolor='black', markeredgewidth=1, color='salmon', markersize=m1_p2*10, zorder=3)

line_m2_p2_back, = ax.plot([x1_p2[0],x2_p2[0]], [y1_p2[0],y2_p2[0]], '-', color='k', lw=4, solid_capstyle='round')
line_m2_p2_front, = ax.plot([x1_p2[0],x2_p2[0]], [y1_p2[0],y2_p2[0]], '-', color='w', lw=2, solid_capstyle='round', zorder=2)
m2_p2_dot, = ax.plot(x2_p2[0], y2_p2[0], 'o', markeredgecolor='black', markeredgewidth=1, color='salmon', markersize=m2_p2*10, zorder=3)

################################################
################################################
################################################

time_template = 'Time = {:3.1f}s'.format
time_text = ax.text(-(L1_p1+L2_p1)*0.25,-(L1_p1+L2_p1)*1.25, time_template(0),fontsize=20, style='italic',bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10})

ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim((-L1_p1-L2_p1)*1.1,(L1_p1+L2_p1)*1.1)
ax.set_ylim((-L1_p1-L2_p1)*1.1,(L1_p1+L2_p1)*1.1)

def animate(i):
    # First pendulum 
    m2_p1_trajectory.set_data(x2_p1[:i], y2_p1[:i])
    line_m1_p1_back.set_data([0,x1_p1[i]],[0,y1_p1[i]])
    line_m1_p1_front.set_data([0,x1_p1[i]],[0,y1_p1[i]])
    line_m2_p1_back.set_data([x1_p1[i],x2_p1[i]],[y1_p1[i],y2_p1[i]])
    line_m2_p1_front.set_data([x1_p1[i],x2_p1[i]],[y1_p1[i],y2_p1[i]])
    m1_p1_dot.set_data(x1_p1[i], y1_p1[i])
    m2_p1_dot.set_data(x2_p1[i], y2_p1[i])
    
    # Second pendulum 
    m2_p2_trajectory.set_data(x2_p2[:i], y2_p2[:i])
    line_m1_p2_back.set_data([0,x1_p2[i]],[0,y1_p2[i]])
    line_m1_p2_front.set_data([0,x1_p2[i]],[0,y1_p2[i]])
    line_m2_p2_back.set_data([x1_p2[i],x2_p2[i]],[y1_p2[i],y2_p2[i]])
    line_m2_p2_front.set_data([x1_p2[i],x2_p2[i]],[y1_p2[i],y2_p2[i]])
    m1_p2_dot.set_data(x1_p2[i], y1_p2[i])
    m2_p2_dot.set_data(x2_p2[i], y2_p2[i])
    time_text.set_text(time_template(t[i]))

fps = 25
every_x_frame = 1 / (delta_t*fps)
an = FuncAnimation(fig, animate, frames= np.arange(0,len(t),int(every_x_frame)), interval=20, repeat=False)
plt.show()

