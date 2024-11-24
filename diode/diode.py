import numpy as np
import matplotlib.pyplot as plt
from constant import *

# Размеры сетки
nx, ny = 100, 100
dx, dy = 1e-4, 1e-4  # Шаг сетки
phi = np.zeros((nx, ny))  # Потенциал

# Граничные условия
phi[:, 0] = 0        # Катод (левый край)
phi[:, -1] = 100     # Анод (правый край)

# Метод итераций (метод Гаусса-Зейделя)
tolerance = 1e-5
while True:  # Итерации
    phi_old = phi.copy()
    phi[1:-1, 1:-1] = 0.25 * (phi[2:, 1:-1] + phi[:-2, 1:-1] + phi[1:-1, 2:] + phi[1:-1, :-2])
    if np.max(np.abs(phi - phi_old)) < tolerance:
        break

# Рассчёт градиента потенциала (электрическое поле)
Ex, Ey = np.gradient(-phi, dx, dy)

x = np.linspace(0, dx * nx, nx)  # Физическая шкала x
y = np.linspace(0, dy * ny, ny)  # Физическая шкала y
plt.figure(figsize=(8, 6))
plt.plot(x, Ex[ny // 2, :], label="E_x вдоль оси X (середина области)")
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.title("Электрическое поле вдоль оси X")
plt.xlabel("X (м)")
plt.ylabel("E_x (В/м)")
plt.legend()
plt.grid()
plt.show()

# Визуализация потенциала
plt.imshow(phi, cmap='hot', origin='lower')
plt.colorbar(label="Электрический потенциал (В)")
plt.title("Распределение потенциала")
plt.show()



# Начальная позиция электрона
x, y = 10, 50  # Начальная позиция в сетке (вблизи катода)
vx, vy = 0, 0  # Начальная скорость

# Шаг времени
dt = 1e-13

# Сохраняем траекторию
trajectory = []

# Симуляция
for _ in range(1000):  # Шаги симуляции
    # Индексы в сетке
    xi, yi = int(x), int(y)
    
    # Ускорение
    ax = e * Ex[xi, yi] / m_e
    ay = e * Ey[xi, yi] / m_e
    
    # Скорость
    vx += ax * dt
    vy += ay * dt
    
    # Позиция
    x += vx * dt / dx
    y += vy * dt / dy
    
    # Сохранение траектории
    trajectory.append((x, y))
    
    # Проверка выхода электрона из области
    if x >= nx - 1 or y >= ny - 1 or x < 0 or y < 0:
        break

# Визуализация траектории
trajectory = np.array(trajectory)
plt.plot(trajectory[:, 0], trajectory[:, 1], marker="o")
plt.title("Траектория электрона")
plt.xlabel("x (сетка)")
plt.ylabel("y (сетка)")
plt.grid(True)
plt.show()