###########################################################################################################
#                                                 IN THE NAME OF ALLAH                                    #
#                               SOIL-PILE INTERACTIONS WITH FINITE DIFFERENCE METHOD                      #
#---------------------------------------------------------------------------------------------------------#
# This Python code models the interaction between a soil and a pile using the finite difference method    #
# to solve the fourth-order differential equation for pile deflection under lateral soil forces.          #
# It computes and visualizes the displacement, soil reaction,                                             #
# shear force, and bending moment distributions along the pile length.                                    #
#                               EQUATION: E * I * (d4y_dx4) + Es * y - Qx                                 #
#---------------------------------------------------------------------------------------------------------#
#                        THIS PROGRAM IS WRITTEN BY SALAR DELAVAR GHASHGHAEI (QASHQAIA)                   #
#                                          EMAIL: SALAR.D.GHASHGHAEI@GMAIL.COM                            #
###########################################################################################################

import numpy as np
import matplotlib.pyplot as plt

# Define constants
E = 2.1e11       # Elastic modulus of the pile (Pa)
I = 8.3e-6       # Moment of inertia of the pile cross-section (m^4)
Es = 1e8         # Modulus of subgrade (soil) reaction (Pa/m)
L = 20.0         # Length of the pile (m)
Qx = 1e4         # Lateral soil force per unit length (N/m)
# Number of nodes and step size
nodes = 200
dx = L / (nodes - 1)

# Define matrices for finite difference method
A = np.zeros((nodes, nodes))  # Coefficient matrix
b = np.zeros(nodes)          # Right-hand side

# Populate the finite difference matrix (fourth-order differential equation)
for i in range(2, nodes - 2):
    A[i, i - 2] = E * I / dx**4
    A[i, i - 1] = -4 * E * I / dx**4
    A[i, i] = 6 * E * I / dx**4 + Es
    A[i, i + 1] = -4 * E * I / dx**4
    A[i, i + 2] = E * I / dx**4
    b[i] = -Qx

# Boundary conditions
A[0, 0] = 1  # Fixed displacement at x=0
A[1, 0:3] = np.array([1, -1, 0]) / dx  # Fixed slope at x=0
A[-1, -1] = 1  # Fixed displacement at x=L
A[-2, -3:] = np.array([0, -1, 1]) / dx  # Fixed slope at x=L

# Solve for displacement
y = np.linalg.solve(A, b)

# Calculate shear force and bending moment
moment = -E * I * np.gradient(np.gradient(y, dx), dx)  # Bending moment
shear = np.gradient(moment, dx)  # Shear force

# Calculate reactions (subgrade reaction)
reactions = Es * y

# Plot results
x = np.linspace(0, L, nodes)

plt.figure(figsize=(16, 12))

# Plot displacements
plt.subplot(2, 2, 1)
plt.plot(x, y, label='Displacement', color='blue')
plt.xlabel('Length along pile (m)')
plt.ylabel('Displacement (m)')
plt.title('Pile Displacement')
plt.grid()
plt.legend()

# Plot reactions
plt.subplot(2, 2, 2)
plt.plot(x, reactions, label='Reaction Force', color='red')
plt.xlabel('Length along pile (m)')
plt.ylabel('Reaction Force (N)')
plt.title('Soil Reaction Forces')
plt.grid()
plt.legend()

# Plot shear force
plt.subplot(2, 2, 3)
plt.plot(x, shear, label='Shear Force', color='green')
plt.xlabel('Length along pile (m)')
plt.ylabel('Shear Force (N)')
plt.title('Shear Force Distribution')
plt.grid()
plt.legend()

# Plot bending moment
plt.subplot(2, 2, 4)
plt.plot(x, moment, label='Bending Moment', color='purple')
plt.xlabel('Length along pile (m)')
plt.ylabel('Bending Moment (Nm)')
plt.title('Bending Moment Distribution')
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
