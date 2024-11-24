import numpy as np
import matplotlib.pyplot as plt
from constant import *


# Given parameters
d = 0.01  # Distance between cathode and anode (m)
U = 100  # Voltage of anode (V)

# Law of three-halves (Child-Langmuir law) for current density j
j = (4 / 9) * epsilon_0 * np.sqrt(2 * e / m_e) * (U**1.5) / (d**2)

# Calculate 'a' from the formula: a^2 = 4πj * sqrt(m / 2e)
a_squared = 4 * pi * j * np.sqrt(m_e / (2 * e))
a = np.sqrt(a_squared)

# Define formulas
def phi(x):
    """Potential phi(x)"""
    return U * x**(4 / 3)/d**(4/3)

def electric_field(x):
    """Electric field E(x) = -d(phi)/dx"""
    return (4 / 3) * (3 / 2) * U * x**(1 / 3)

def concentration(x):
    """Electron concentration n(x)"""
    potential = phi(x)
    velocity = np.sqrt((2 * e * potential) / m_e)
    return j / (e * velocity)

# Generate x values
x_values = np.linspace(0.001, d, 100)  # Avoid x=0 to prevent singularities

# Compute values
phi_values = phi(x_values)
E_values = electric_field(x_values)
n_values = concentration(x_values)

# Plot results
plt.figure(figsize=(12, 8))

# Potential phi(x)
plt.subplot(3, 1, 1)
plt.plot(x_values, phi_values, label=r"$\phi(x)$ (Potential)", color='blue')
plt.title("потенциал $\phi(x)$")
plt.xlabel("x (m)")
plt.ylabel("потенциал (V)")
plt.grid(True)
plt.legend()

# Electric field E(x)
plt.subplot(3, 1, 2)
plt.plot(x_values, E_values , label=r"$E(x)$ (Electric Field)", color='red')
plt.title("электрическое поле $E(x)$")
plt.xlabel("x (m)")
plt.ylabel("электрическое поле (V/m)")
plt.grid(True)
plt.legend()

# Electron concentration n(x)
plt.subplot(3, 1, 3)
plt.plot(x_values, n_values, label=r"$n(x)$ (Electron Concentration)", color='green')
plt.title("концентрация электронов $n(x)$")
plt.xlabel("x (m)")
plt.ylabel("концентрация")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()