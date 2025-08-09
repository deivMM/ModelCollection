import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Parameters ---
box_size = 10           # Box is from (0,0) to (10,10)
radius = 0.3            # Ball radius
pos = np.array([5, 5], dtype=float)
vel = np.array([2, 3], dtype=float)  # Initial velocity
c = .5 # Coefficient of restitution


dt = 0.05               # Time step
tmax = 100
nt = int(tmax/dt)
t = np.linspace(0,tmax,nt+1)
k = -np.log(2)/2

# --- Set up the figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), facecolor='.85')
time_template = 'Time = {:4.2f} s.'.format
text_args = dict(fontsize=15,ha='center', va='center', style='italic',bbox={'facecolor': 'white', 'alpha': 1, 'pad': 5})
time_text = ax1.text(10, 11, time_template(0),**text_args)


ax1.set_xlim(0, box_size)
ax1.set_ylim(0, box_size)
ax2.set_xlim(0, tmax)
ax2.set_ylim(0, np.linalg.norm(vel) * 1.1)

ax1.set_xticks([])
ax1.set_yticks([])
ball = plt.Circle(pos, radius, fc='blue')
lineax2, = ax2.plot([],[],'b')

ax1.add_patch(ball)
ax1.set_aspect('equal', adjustable='box')

vel_list = []

def init():
    ball.center = pos
    time_text.set_text(time_template(0))
    return ball, time_text

def anim(n):
    time_text.set_text(time_template(t[n]))
    global pos, vel
    pos += vel * dt

    # Check collisions with walls
    for i in [0, 1]:
        if pos[i] - radius <= 0:
            pos[i] = radius
            vel[i] *= -c
        elif pos[i] + radius >= box_size:
            pos[i] = box_size - radius
            vel[i] *= -c
    
    vel_list.append(float(np.linalg.norm(vel)))
    lineax2.set_data(t[:n+1], vel_list)
    ball.center = pos
    return ball,

an = FuncAnimation(fig, anim, frames=len(t), init_func=init,interval=10, repeat=False)
# plt.gca().set_aspect('equal', adjustable='box')
plt.show()
