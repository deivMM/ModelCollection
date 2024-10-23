# when we're in pylab mode, the next two imports are not necessary
# we do it here for correctness sake, iow your code will also run without pylab mode
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

# gravitational acceleration on Earth in m*s^-2
g = 9.80665
#g = 1.6249
# acceleration vector due to g
ag = np.array((0,-g))
# coefficient of restitution (ratio of velocity after and before bounce)
# see http://en.wikipedia.org/wiki/Coefficient_of_restitution
cor = 0.6

# bounds of the room
xlim = (0,30)
ylim = (0,30)

# 1 millisecond delta t
delta_t = 0.001
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=xlim, ylim=ylim)
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], xlim=xlim, ylim=ylim)


# in Python 2.7 we have to derive from object to have new-style classes
# in Python 3 this is still valid, but not necessary, as all classes are new-style
class Ball(object):

    def __init__(self, xy, v):
        """
        :param xy: Initial position.
        :param v: Initial velocity.
        """
        self.xy = np.array(xy)
        self.v = np.array(v)

        self.scatter, = ax.plot([], [], 'o', markersize=5, color='b')

    def update(self):
        if self.xy[0] <= xlim[0]:
            # hit the left wall, reflect x component
            self.v[0] = cor * np.abs(self.v[0])

        elif self.xy[0] >= xlim[1]:
            self.v[0] = - cor * np.abs(self.v[0])

        if self.xy[1] <= ylim[0]:
            # hit the left wall, reflect y component
            self.v[1] = cor * np.abs(self.v[1])

        elif self.xy[1] >= ylim[1]:
            self.v[1] = - cor * np.abs(self.v[1])

        # delta t is 0.1
        delta_v = delta_t * ag
        self.v += delta_v


        self.xy += self.v
# Recorta los valores para que esté siempre dentro de los limites
        self.xy[0] = np.clip(self.xy[0], xlim[0], xlim[1])
        self.xy[1] = np.clip(self.xy[1], ylim[0], ylim[1])

        self.scatter.set_data(self.xy)

n = 10
balls = [Ball((random.random()*30,random.random()*30), (random.random(),random.random())) for i in range(n)]

def animate(t):
    # t is time in seconds
    for ball in balls:
        ball.update()
    # have to return an iterable
    return [ball.scatter for ball in balls]

# interval in milliseconds
# we're watching in slow motion (delta t is shorter than interval)
ani = animation.FuncAnimation(fig, animate, np.arange(0,100,delta_t), interval=10, blit=True)
plt.show()
