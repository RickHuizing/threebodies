# body mass
import numpy as np

from data_generation.tbp_energy_calculations import calculate_potential_energy, calculate_kinetic_energy

# Newton constant
G = np.longfloat(1.0)

# x = [0, 0, 0]
# y = [1, -1, 0]
# vx = [0.3471, 0.3471, -2 * 0.3471]
# vy = [0.5327, 0.5327, -2 * 0.5327]

x = [1.000000000000000000e+00, -1.051669950659417374e-03, -9.989483300493405826e-01]
y = [0.000000000000000000e+00, 4.608633953081185952e-01, -4.608633953081185952e-01]
vx = [0.000000000000000000e+00, 0.000000000000000000e+00, 0.000000000000000000e+00]
vy = [0.000000000000000000e+00, 0.000000000000000000e+00, 0.000000000000000000e+00]

x = [9.999999964738484071e-01, -1.051668691160122368e-03, -9.989483277826882723e-01]
y = [1.047401366887073294e-09, 4.608633927448660406e-01, -4.608633937922673729e-01]
vx = [-8.815379085910412442e-05, 3.148748245738279945e-05, 5.666630840172133174e-05]
vy = [2.618503420714357474e-05, -6.408131440074255373e-05, 3.789628019359897221e-05]

x = [1.000000000000000000e+00, -3.811232615101186605e-01, -6.188767384898813395e-01]
y = [0.000000000000000000e+00, 6.208501776207997480e-01, -6.208501776207997480e-01]
# x = [1.000000000000000000e+00, -3.839371696226984154e-02, -9.616062830377301029e-01]
# y = [0.000000000000000000e+00, 4.010315235170663350e-01, -4.010315235170663350e-01]
vx = [0.000000000000000000e+00, 0.000000000000000000e+00, 0.000000000000000000e+00]
vy = [0.000000000000000000e+00, 0.000000000000000000e+00, 0.000000000000000000e+00]

locations = np.array([[x[i], y[i]] for i in range(3)])
velocities = np.array([[vx[i], vy[i]] for i in range(3)])

# body mass
M = np.array([1.0, 1.0, 1.0], float)

potential_energy = calculate_potential_energy(G, M, locations)

kinetic_energy = calculate_kinetic_energy(M, velocities)

print(potential_energy)
print(kinetic_energy)
print(potential_energy + kinetic_energy)
