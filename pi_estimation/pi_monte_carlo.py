# Monte Carlo Pi Estimation
import time
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

npoints = 5000
w = 100
pi_estimation = []

def animate(i):
    x_rand = random.rand(i)  # Random x coordinate
    y_rand = random.rand(i)  # Random y coordinate
    indexes = (x_rand-0.5)**2+(y_rand- 0.5)**2<0.25
    xin = x_rand[indexes]
    yin = y_rand[indexes]
    xout = np.delete(x_rand,indexes)
    yout = np.delete(y_rand,indexes)
    pi_estimation.append(4*len(xin)/i)
    if not i % 100:
        time.sleep(.1)
        lin.set_data(xin,yin)
        lout.set_data(xout,yout)
        l_pi_est.set_data(np.linspace(100,i,len(pi_estimation)),pi_estimation)
        t1.set_text(points_template(i))
        t2.set_text(pi_template(pi_estimation[-1],abs(np.pi-pi_estimation[-1])))
        if len(pi_estimation)>200:
            media_movil = np.convolve(pi_estimation, np.ones(w), 'valid') / w
            x_media_movil = np.arange(100,100+len(pi_estimation)+1)[int(np.floor(w/2)):-int(np.ceil(w/2))]
            l_pi_est_mean.set_data(x_media_movil,media_movil)

def init():
    lin.set_data([], [])
    lout.set_data([], [])
    l_pi_est.set_data([], [])
    return lin,lout

f= plt.figure(figsize=(12,7),facecolor='.85')
spec = f.add_gridspec(6,2)

ax11 = f.add_subplot(spec[:1, :1])
ax12 = f.add_subplot(spec[:1, 1:])
ax21 = f.add_subplot(spec[1:, :1])
ax22 = f.add_subplot(spec[1:, 1:])

points_template = 'Nº of points = {:6d}'.format
pi_template = '  $\pi_{{est}}$ = {:8.6f}\nerror = {:8.6f}'.format

text_args = dict(fontsize=20,ha='center', va='center', style='italic',bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10})

ax21.add_patch(plt.Circle((0.5, 0.5), radius=.5, fill=False, linewidth = 2, alpha =.3))
lin, = ax21.plot([], [], 'go', markersize=1)
lout, =ax21.plot([], [], 'ro', markersize=1)
l_pi_est, = ax22.plot([], [],linewidth=.1)
l_pi_est_mean, = ax22.plot([], [],'k')

t1 = ax11.text(.5,.5, points_template(0),**text_args)
t2 = ax12.text(.5,.5, pi_template(0,0),**text_args)

ax21.axis([0,1,0,1])
ax21.set_xticks([0.,0.5,1.])
ax21.set_yticks([0.,0.5,1.])
ax22.axhline(y=np.pi, color='r',alpha=.3)

ax22.axis([100,npoints,2.8,3.5])
ax22.set_yticks([2.6,2.8,3,3.2,3.4,3.6])

ax11.axis('off')
ax12.axis('off')
ax21.set_aspect('equal', 'box')
ax22.text(npoints+.04*npoints,np.pi, 'π',fontsize=20,ha='center', va='center')
ax22.legend([l_pi_est_mean],['mean'],loc=1)

f.suptitle('Estimating Pi using Monte Carlo',fontsize=20,x=0.5,y=.95,weight='semibold')
an = FuncAnimation(f, animate, frames= np.arange(100,npoints+1),init_func=init, interval=1, repeat=False)
plt.show()
