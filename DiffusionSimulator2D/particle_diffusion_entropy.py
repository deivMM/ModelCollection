import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Parámetros
n = 200  # number of particles
L = 10 # size of the box
r = 0.1         # radio de partícula
dt = 0.05
time = 10 # simulation time

grid_size = 20  # Para el cálculo de entropía
steps = int(time / dt)  # número de pasos de tiempo

# Inicialización
np.random.seed(1)
percent = 0.9  # 0 muy separado y 1 muy pegado
pos = np.random.uniform(r + percent * (L * 0.5 - r), L * 0.5 + (1 - percent) * (L * 0.5 - r), size=(n, 2))
vel = np.random.uniform(-1, 1, size=(n, 2))

fig, (ax_particles, ax_entropy) = plt.subplots(1, 2, figsize=(10, 6), facecolor='.85')
fig.subplots_adjust(top=0.9)

ax_time = fig.add_axes([0, 0.9, 1, 0.08])  # y=0.90 está justo debajo del top=0.88
ax_time.axis("off")

time_template = 'Time = {:4.2f} s.'.format
text_args = dict(fontsize=15, ha='center', va='center', style='italic',
                 bbox={'facecolor': 'white', 'alpha': 1, 'pad': 5})
time_text = ax_time.text(0.5, 0.5, time_template(0), transform=ax_time.transAxes, **text_args)

particles, = ax_particles.plot([], [], 'bo', ms=4)
ax_particles.set_xlim(0, L)
ax_particles.set_ylim(0, L)
ax_particles.set_aspect('equal')
ax_particles.set_xticks([])
ax_particles.set_yticks([])

# Entropía: curva
entropias = []
line_entropy, = ax_entropy.plot([], [], 'r-')
ax_entropy.set_aspect('equal')
ax_entropy.set_xlim(0, steps * dt)
ax_entropy.set_ylim(0, 10)  # puedes ajustar según lo que veas
ax_entropy.set_xlabel("Time (s)")
ax_entropy.set_ylabel("Entropy")

def colision_elastica(i, j):
    rij = pos[i] - pos[j]
    vij = vel[i] - vel[j]
    dist_sq = np.dot(rij, rij)
    if dist_sq == 0:
        return
    factor = np.dot(vij, rij) / dist_sq
    vel[i] -= factor * rij
    vel[j] += factor * rij

def calcular_entropia(pos, L, grid_size):
    # matriz 2D con numero de partículas por celda.
    H, _, _ = np.histogram2d(pos[:, 0], pos[:, 1], bins=grid_size, range=[[0, L], [0, L]])
    # Convierte la matriz H en un vector 1D | lista de cantidades de partículas por celda.
    p = H.flatten() 
    # 1D array de probabilidades, eliminando las celdas con 0 partículas.
    p = p[p > 0] / np.sum(p) 
    # Calculo de la entropía de Shannon.
    S = -np.sum(p * np.log(p))
    return S

def init():
    particles.set_data([], [])
    line_entropy.set_data([], [])
    time_text.set_text(time_template(0))
    return particles, line_entropy, time_text

def update(frame):
    global pos, vel

    # Actualizar posiciones
    pos += vel * dt

    # Rebotes con paredes
    for i in range(n):
        for d in range(2):
            if pos[i, d] - r <= 0 or pos[i, d] + r >= L:
                vel[i, d] *= -1
                pos[i, d] = np.clip(pos[i, d], r, L - r)

    # Colisiones entre partículas
    for i in range(n):
        for j in range(i + 1, n):
            rij = pos[i] - pos[j]
            dist = np.linalg.norm(rij)
            if dist < 2 * r:
                colision_elastica(i, j)
                if dist > 0:
                    overlap = 2 * r - dist
                    direction = rij / dist
                    pos[i] += 0.5 * overlap * direction
                    pos[j] -= 0.5 * overlap * direction

    # Actualizar partículas
    particles.set_data(pos[:, 0], pos[:, 1])

    # Calcular y actualizar entropía
    S = calcular_entropia(pos, L, grid_size)
    entropias.append(S)
    t_vals = np.arange(len(entropias)) * dt
    line_entropy.set_data(t_vals, entropias)
    
    time_text.set_text(time_template(t_vals[frame]))
    
    # Ajustar eje y si es necesario
    if S > ax_entropy.get_ylim()[1]:
        ax_entropy.set_ylim(0, S + 1)

    return [particles, line_entropy, time_text]


ani = FuncAnimation(fig, update, frames=steps, init_func=init, interval=50, blit=True, repeat=False)

plt.tight_layout()

print('guardando la animación ...')
writer = PillowWriter(fps=40)
ani.save("particle_diffusion.gif", writer=writer)
print('Animación guardada !!!')

# Mostrar la figura
plt.show()