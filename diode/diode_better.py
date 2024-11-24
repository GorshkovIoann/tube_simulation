import numpy as np
import matplotlib.pyplot as plt
from constant import *

# Параметры задачи
L = 1e-3  # Длина диода (1 мм)
V_anode = 100  # Напряжение на аноде (В)
dx = 1e-5  # Шаг сетки (10 мкм)
dt = 1e-12  # Шаг времени (1 пс)
n_steps = 300  # Количество временных шагов
n_points = int(L / dx)  # Количество точек сетки

# Расчет плотности тока по правилу 3/2
J = (4 / 9) * epsilon_0 * np.sqrt(2 * e / m_e) * (V_anode**1.5) / (L**2)
S = 1e-3  # Площадь катода (1 мм²)
Q_emitted = J * dt * S  # Заряд одного испускаемого электрона

# Начальные условия
phi = np.zeros(n_points)  # Линейное распределение потенциала
phi[-1] = V_anode
rho = np.zeros(n_points)  # Плотность заряда (вначале нулевая)
electrons = []  # Список электронов (каждый с позицией и зарядом)

# Функции

def solwve_step_poisson(phi, rho, dx, epsilon_0, tol=1e-6):
    for i in range(1, n_points - 1):
        phi_new = phi.copy()
        phi_old = phi_new.copy()
        phi_new[i] = 0.5 * (phi_old[i - 1] + phi_old[i + 1] - dx ** rho[i] / epsilon_0)
        
    return phi_new

def solve_poisson(phi, rho, dx, epsilon_0, tol=1e-6):
    """
    Решение уравнения Пуассона: Δφ = -ρ/ε₀
    """
    phi_new = phi.copy()
    error = tol + 1
    while error > tol:
        phi[-1] = V_anode
        phi_old = phi_new.copy()
        for i in range(1, n_points - 1):
            phi_new[i] = 0.5 * (phi_old[i - 1] + phi_old[i + 1] - dx**2*rho[i]/epsilon_0)
        error = np.max(np.abs(phi_new - phi_old))
    return phi_new

def compute_electric_field(phi, dx):
    """
    Расчет электрического поля как -градиент потенциала.
    """
    E = -np.gradient(phi, dx)
    return E

def update_electrons(electrons, E, dt, dx):
    """
    Обновление положения и скорости электронов.
    """
    for electron in electrons:
        x_idx = int(electron['x'] / dx)
        if 0 <= x_idx < len(E):
            F = -e * E[x_idx]
            a = F / m_e
            electron['v'] += a * dt
            electron['x'] += electron['v'] * dt

def update_charge_density(electrons, rho, dx):
    """
    Обновление плотности заряда в каждой ячейке сетки.
    """
    rho.fill(0)  # Сбрасываем плотность заряда
    for electron in electrons:
        x_idx = int(electron['x'] / dx)
        if 0 <= x_idx < len(rho):
            rho[x_idx] += Q_emitted / dx

def inject_electron(electrons):
    """
    Инжекция заряда на катоде.
    """
    electrons.append({'x': 0, 'v': 0})  # Добавляем электрон с начальной скоростью 0

# Основной цикл моделирования
phi_history = []
E_history = []
v_history = []
phi = solve_poisson(phi, rho, dx, epsilon_0)

for step in range(n_steps):
    # Инжектируем один электрон
    inject_electron(electrons)
    
    # Обновляем плотность заряда
    update_charge_density(electrons, rho, dx)
    
    # Решаем уравнение Пуассона
    phi = solve_poisson(phi, rho, dx, epsilon_0)
    
    # Вычисляем электрическое поле
    E = compute_electric_field(phi, dx)
    
    # Обновляем движение электронов
    update_electrons(electrons, E, dt, dx)
    
    # Сохраняем результаты
    phi_history.append(phi.copy())
    E_history.append(E.copy())
    v_history.append([electron['v'] for electron in electrons])



# Потенциал
plt.figure(figsize=(10, 6))
plt.plot(np.linspace(0, L, n_points), phi_history[-1] - 1000000 * rho)
plt.title("Распределение потенциала")
plt.xlabel("Положение (м)")
plt.ylabel("Потенциал (В)")
plt.grid()
plt.show()

# плотность заряда
plt.figure(figsize=(10, 6))
plt.plot(np.linspace(0, L, n_points), -rho)
plt.title("плотность заряда")
plt.xlabel("Положение (м)")
plt.ylabel("плотность заряда (Кл/м)")
plt.grid()
plt.show()