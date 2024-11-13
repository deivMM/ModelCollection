import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def calc_1D_flux(a,b,nx,tmax,alfa,k,fa,fb,T0):
    m = (b-a)/nx
    x = np.linspace(0,b,nx+1)
    nt = int(tmax/0.05)
    p = tmax/nt
    lamb = alfa*p/m**2
    t = np.linspace(0,tmax,nt+1)
    temp = np.zeros((nt+1, nx+1)) #t, x
    temp[0] = T0
    for t_ in range(nt):
        temp[t_+1,0]=(1-2*lamb)*temp[t_,0]+2*lamb*(temp[t_,1]+fa*m/k)
        temp[t_+1,-1]=(1-2*lamb)*temp[t_,-1]+2*lamb*(temp[t_,-2]+fb*m/k)
        for x_ in range(1,nx):
            temp[t_+1,x_] = (1-2*lamb)*temp[t_,x_]+lamb*(temp[t_,x_+1]+temp[t_,x_-1])
    return temp,t,x

a = 0
b = 0.2
T0 = 20
nx = 20
tmax = 10
density = 2700 #  density (SI-> kg/m3)
cp = 900 # Specific heat (SI-> J/kgK)
k = 40 #  thermal conductivity (SI-> W/mk)
alfa = k/(density*cp) # Thermal diffusivity (SI-> m^2/s)

fa = 100000
fb = -50000
res,t,x = calc_1D_flux(a,b,nx,tmax,alfa,k,fa,fb,T0)

p_estudio = 0.02
limite = round(1.05*np.amax(res),-1)

f, (ax1,ax2) = plt.subplots(2,1,figsize=(7,8),facecolor='.85')
time_template = 'Time = {:4.2f} s.'.format
text_args = dict(fontsize=15,ha='center', va='center', style='italic',bbox={'facecolor': 'white', 'alpha': 1, 'pad': 5})
time_text = ax1.text(b*.5,limite+limite*.1, time_template(0),**text_args)
ax1.set_xlabel('Height (mm)',fontsize=12)
ax1.set_ylabel('Temp. ($^\circ$C)',fontsize=12)
ax2.set_xlabel('Time (s)',fontsize=12)
ax2.set_ylabel('Temp. ($^\circ$C)',fontsize=12)
ax1.set_ylim(0, limite)
ax1.set_xlim(0, b)

line, = ax1.plot([],[], 'k')
p_est_scat = ax1.scatter(p_estudio, 20, c='blue',s=200,alpha=.2)
scat = ax1.scatter([],[], c='g',s=10)
ax1.plot(x,res[0],'k',alpha=.2)
ax1.scatter(x, res[0], c='k',s=10,alpha=.2)

f.suptitle('1D Heat Equation',fontsize=14,x=0.5,y=.98,weight='semibold')
index = np.where(x == p_estudio)
ax2.plot(t,res[:,index[0]],'b',linewidth=.5,alpha=.2)
lineax2, = ax2.plot([],[],'b')
scatax2 = ax2.scatter([],[], c='b',s=20)

def init():
    pass

def anim(i):
    time_text.set_text(time_template(t[i]))
    line.set_data(x,res[i])
    scat.set_offsets(np.c_[x,res[i]])
    p_est_scat.set_offsets(np.c_[p_estudio,res[i,index[0]]])
    lineax2.set_data(t[:i],res[:i,index[0]])
    scatax2.set_offsets(np.c_[t[i],res[i,index][0]])
    return line

an = FuncAnimation(f, anim, frames=len(t), init_func=init,interval=10, repeat=False)
plt.show()
################################################
an.save("Heat_equation_gif.gif", writer=PillowWriter(fps=50))
print('gif created')