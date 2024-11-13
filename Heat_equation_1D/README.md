![' Heat equation 1D gif'](./Heat_ecuation_gif.gif)

# Numerical model of heat equation
Numerical model of the heat equation

Temperature $\LARGE\to  T = f(x,t)[ºC]$

Time $\LARGE\to t[s]$

Thermal diffusivity $\LARGE\to \alpha=\frac{k}{\rho c_p}[\frac{m^2}{s}]$


$$\LARGE\nabla^{2}T+\frac{q}{k}=\frac{1}{\alpha}\frac{\partial T}{\partial t}$$

$$\LARGE\frac{\partial^2 T}{\partial x^2}+\frac{\partial^2 T}{\partial y^2}+\frac{\partial^2 T}{\partial z^2}+\frac{q}{k}=\frac{1}{\alpha}\frac{\partial T}{\partial t}$$

$$\LARGE\frac{\partial^2 T}{\partial x^2}+\frac{q}{k}=\frac{1}{\alpha}\frac{\partial T}{\partial t}$$


$$\LARGE\frac{k}{c_p\rho}\underset{dif.\ central}{\underbrace{\frac{\partial^2 T}{\partial x^2}}}+\frac{q}{c_p\rho} = \underset{dif.\ progr.}{\underbrace{\frac{\partial T}{\partial t}}}$$

$$\LARGE\frac{k}{c_p\rho}\frac{T_{m+1,p}-2T_{m,p}+T_{m-1,p}}{\Delta x^2} +\frac{q}{c_p\rho} = \frac{T_{m,p+1}-T{m,p}}{\Delta t}$$

Multiplicando a toda la expresión anterior por k y llamando a $\LARGE\lambda=\frac{\alpha\Delta t}{\Delta x^2}$ se obtiene:

$$\LARGE\lambda (T_{m+1,p}-2T_{m,p}+T_{m-1,p})+\frac{q\Delta t}{c_p\rho} = T_{m,p+1}-T_{m,p}$$

$$\boxed{\LARGE T_{m,p+1}=\lambda (T_{m+1,p}-2T_{m,p}+T_{m-1,p})+\frac{q\Delta t}{c_p\rho}+T_{m,p}}$$

