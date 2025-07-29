
!['2D diffusion model'](./particle_diffusion.gif)

This project simulates the spatial diffusion of particles within a closed 2D box and analyzes the evolution of entropy over time using Shannon's entropy formula.
Shannon entropy formula to quantify disorder:

$$H = -\sum_{i=1}^{n} p_i \ln p_i$$

Where:
- $p_i$ is the probability that a particle is located in cell $i$, based on a 2D histogram of the box.
- Entropy reaches its maximum value when the particles are uniformly distributed across all cells.
