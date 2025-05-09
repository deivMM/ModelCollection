import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Parámetros
n = 200
L = 10
r = 0.1         # radio de partícula
dt = 0.05
steps = 500
grid_size = 20  # Para el cálculo de entropía

# Inicialización
np.random.seed(1)
percent = 0.8  # 0 muy separado y 1 muy pegado
pos = np.random.uniform(r + percent * (L * 0.5 - r), L * 0.5 + (1 - percent) * (L * 0.5 - r), size=(n, 2))
vel = np.random.uniform(-1, 1, size=(n, 2))

# Preparar figura con 2 subplots
fig, (ax_particles, ax_entropy) = plt.subplots(1, 2, figsize=(10, 5),facecolor='.85')
particles, = ax_particles.plot([], [], 'bo', ms=4)
ax_particles.set_xlim(0, L)
ax_particles.set_ylim(0, L)
ax_particles.set_aspect('equal')
ax_particles.set_xticks([])
ax_particles.set_yticks([])

# Entropía: curva
entropias = []
line_entropy, = ax_entropy.plot([], [], 'r-')
ax_entropy.set_xlim(0, steps * dt)
ax_entropy.set_ylim(0, 10)  # puedes ajustar según lo que veas
ax_entropy.set_xlabel("Tiempo")
ax_entropy.set_ylabel("Entropía")

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
    H, _, _ = np.histogram2d(pos[:, 0], pos[:, 1], bins=grid_size, range=[[0, L], [0, L]])
    p = H.flatten()
    p = p[p > 0] / np.sum(p)
    S = -np.sum(p * np.log(p))
    return S

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

    # Ajustar eje y si es necesario
    if S > ax_entropy.get_ylim()[1]:
        ax_entropy.set_ylim(0, S + 1)

    return [particles, line_entropy]

ani = FuncAnimation(fig, update, frames=steps, interval=50, blit=True, repeat=False)

plt.tight_layout()

# print('guardando la animación ...')
# writer = PillowWriter(fps=40)
# ani.save("particle_diffusion.gif", writer=writer)
# print('Animación guardada !!!')

# Mostrar la figura
plt.show()