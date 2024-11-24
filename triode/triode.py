import numpy as np
import matplotlib.pyplot as plt
from constant import *

# Размеры сетки
nx, ny = 100, 100
dx, dy = 1e-4, 1e-4  # Шаг сетки в метрах
phi = np.zeros((nx, ny))  # Начальное значение потенциала

# Граничные условия
phi[:, 0] = 0        # Катод (левый край)
phi[:, -1] = 100     # Анод (правый край)

# Сетка (сеточный электрод)
grid_y = ny // 2  # Положение сетки (по вертикали)
phi[:, grid_y] = 50  # Потенциал сетки (50 В)

# Метод итераций (Гаусса-Зейделя)
tolerance = 1e-5
for _ in range(10000):  # Максимум 10000 итераций
    phi_old = phi.copy()
    phi[1:-1, 1:-1] = 0.25 * (phi[2:, 1:-1] + phi[:-2, 1:-1] + phi[1:-1, 2:] + phi[1:-1, :-2])
    phi[:, grid_y] = 50
    if np.max(np.abs(phi - phi_old)) < tolerance:
        break

# Расчёт электрического поля
Ex, Ey = np.gradient(-phi, dx, dy)

# Визуализация потенциала
x = np.linspace(0, dx * nx, nx)  # Физическая шкала x
y = np.linspace(0, dy * ny, ny)  # Физическая шкала y
plt.figure(figsize=(8, 6))
plt.imshow(phi, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='hot')
plt.colorbar(label="Электрический потенциал (В)")
plt.title("Распределение потенциала (сетка + анод + катод)")
plt.xlabel("X (м)")
plt.ylabel("Y (м)")
plt.show()



plt.contour(x, y, phi, levels=20, cmap='coolwarm')  # Изолинии потенциала
plt.quiver(x, y, Ex, Ey, scale=50, color='black')  # Линии электрического поля
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(x, Ex[ny // 2, :], label="E_x вдоль оси X (середина области)")
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.title("Направление электрического поля вдоль оси X")
plt.xlabel("X (м)")
plt.ylabel("E_x (В/м)")
plt.legend()
plt.grid()
plt.show()


x, y = 10, grid_y - 5  
vx, vy = 0, 0 

dt = 1e-13


trajectory = []


for _ in range(10000):  

    xi, yi = int(x), int(y)
    

    ax = e * Ex[xi, yi] / m_e
    ay = e * Ey[xi, yi] / m_e
    

    vx += ax * dt
    vy += ay * dt
    
   
    x += vx * dt / dx
    y += vy * dt / dy
    

    trajectory.append((x * dx, y * dy))  

    if x >= nx - 1 or y >= ny - 1 or x < 0 or y < 0:
        break


trajectory = np.array(trajectory)
plt.figure(figsize=(8, 6))
plt.plot(trajectory[:, 0], trajectory[:, 1], marker="o", label="Траектория")
plt.title("Траектория электрона в триоде")
plt.xlabel("X (м)")
plt.ylabel("Y (м)")
plt.grid(True)
plt.legend()
plt.show()


electric_field_x, electric_field_y = np.gradient(-phi)
electric_field_y = -electric_field_y 


magnitude = np.sqrt(electric_field_x**2 + electric_field_y**2) + 1e-9  
electric_field_x_normalized = electric_field_x / magnitude
electric_field_y_normalized = electric_field_y / magnitude


plt.figure(figsize=(10, 6))
plt.contourf(phi, levels=50, cmap="inferno")
plt.colorbar(label="Potential (V)")
plt.title("Corrected Electric Field Orientation and Potential Distribution")
plt.xlabel("x (grid points)")
plt.ylabel("y (grid points)")
n
plt.quiver(
    x, y, 
    electric_field_x_normalized, electric_field_y_normalized, 
    color="cyan", scale=20, pivot='mid'
)

plt.show()