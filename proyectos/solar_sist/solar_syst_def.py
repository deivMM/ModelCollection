import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import combinations
import math

G = 1
fig, ((ax1,ax2)) = plt.subplots(1,2,figsize=(12,6),facecolor='lightgrey')
fig.suptitle('SOLAR SYSTEM MODEL', fontsize=20,weight='bold')
plt.subplots_adjust(wspace=0.25, hspace=1)
t_title = ax1.set_title('', fontsize=15)
ax2.set_title('Energy balance', fontsize=15)

T = .07
dt = 0.0001
dt_guargar = 0.0001
t = np.arange(0,T+1e-5,dt)

t_guardar = np.arange(0,T+dt_guargar,dt_guargar)
t_guardar[-1]=T

ax1.set_xlim(-1.5,1.5)
ax1.set_ylim(-1.5,1.5)
ax2.set_xlim(0,T)
ax2.set_ylim(-22000,10000)

class Body:
    def __init__(self,pos,mass,mo,col):
        self.pos = np.array(pos)
        self.mass = mass
        self.mo = np.array(mo)
        self.col = col
        self.res = {'x':[], 'y':[], 'ke':[], 'gpe':[]}
        self.orbit, = ax1.plot([], [],color=self.col, markersize=1)
        self.b_pos = ax1.scatter(0,0,s=10,color=self.col)
        self.ke_pl, = ax2.plot([], [],color=self.col, markersize=1)
        self.gpe_pl, = ax2.plot([], [],color=self.col, linestyle='--', markersize=1)

    def update(self,bodies):
        for body in bodies:
            r_vec = self.pos-body.pos
            r_mag = np.linalg.norm(r_vec)
            r_hat = r_vec/r_mag
            force_mag = G*self.mass*body.mass/r_mag**2
            force = -force_mag*r_hat

            self.mo = self.mo + force*dt
            self.pos = self.pos + self.mo/self.mass*dt
            self.ke = 0.5*np.linalg.norm(self.mo)**2/self.mass
            self.gpe = -G*self.mass*body.mass/r_mag

    def save(self):
        self.res['x'].append(self.pos[0])
        self.res['y'].append(self.pos[1])
        self.res['ke'].append(self.ke)
        self.res['gpe'].append(self.gpe)

star = Body([0,0,0],2000,[0,0,0],'black')
planet1 = Body([1,0,0],1,[0,30,0],'blue')
planet2 = Body([.5,0,0],1,[0,25,0],'green')
bodies = [star,planet1,planet2]

c = list(combinations(bodies, len(bodies)-1))

for i in range(len(t)):
    for n,e in enumerate(bodies):
        e.update(c[-1-n])
        if i%math.ceil(dt_guargar/dt)==0:
            e.save()

def init():
    pass

def anim(i):
    t_title.set_text('Time: {0:.3f} sec.'.format(t_guardar[i]))

    for b in bodies:
        b.orbit.set_data(b.res['x'][:i],b.res['y'][:i])
        b.b_pos.set_offsets([b.res['x'][i],b.res['y'][i]])
        b.ke_pl.set_data(t_guardar[:i],b.res['ke'][:i])
        b.gpe_pl.set_data(t_guardar[:i],b.res['gpe'][:i])

an = FuncAnimation(fig, anim, frames=range(len(t_guardar)), init_func=init,interval=1, repeat=False)
plt.show()
