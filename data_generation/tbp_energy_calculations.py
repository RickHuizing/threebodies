import numpy as np
from matplotlib import pyplot as plt

from data_generation import Three_body_2D_Rick

"""
CALCULATIONS FOUND IN https://fse.studenttheses.ub.rug.nl/8656/1/Math_Drs_1998_BOldeman.CV.pdf
"""


def energy_values(G: float, M: np.ndarray, locations: np.ndarray, velocities: np.ndarray):
    potential_energy = calculate_potential_energy(G, M, locations)
    kinetic_energy = calculate_kinetic_energy(M, velocities)
    return [potential_energy, kinetic_energy, potential_energy + kinetic_energy]


def calculate_total_system_energy(G: float, M: np.ndarray, locations: np.ndarray, velocities: np.ndarray):
    """
    calculate the total system energy of a three body system. Total system energy should stay constant in a TBP
    :param G: gravitational constant
    :param M: masses of the 3 bodies
    :param locations: (x, y) locations of the 3 bodies
    :param velocities: (x, y) velocities of the 3 bodies
    :return:
    """
    return calculate_potential_energy(G, M, locations) + calculate_kinetic_energy(M, velocities)


def calculate_potential_energy(G: float, M: np.ndarray, locations: np.ndarray):
    """
    Calculate the potential energy of a three body system
    :param G: gravitational constant
    :param M: masses of the 3 bodies
    :param locations: (x, y) locations of the 3 bodies
    :return:
    """
    assert M.shape == (3,)
    assert locations.shape == (3, 2)

    return -G * sum(
        0 if i == j else
        (M[i] * M[j]) / np.linalg.norm(locations[i] - locations[j], 2)
        for i in range(3) for j in range(3))


def calculate_kinetic_energy(M: np.ndarray, velocities: np.ndarray):
    """
    Calculate the kinetic energy of a three body system
    :param M: masses of the 3 bodies
    :param velocities: (x, y) velocities of the 3 bodies
    :return:
    """
    return sum(M[i] * (np.linalg.norm(velocities[i], 2) ** 2) / 2 for i in range(3))


def visualize_dataset(x, y, vx, vy, G, M, down_sample_factor=1000):
    """
    calculate energy and show plots
    """
    # down sample using slicing: list[start:stop:step]
    x = x[::down_sample_factor]
    y = y[::down_sample_factor]
    vx = vx[::down_sample_factor]
    vy = vy[::down_sample_factor]

    # potential, kinetic and system energy
    energy = np.ndarray(dtype=float, shape=(x.shape[0], 3))
    for i in range(energy.shape[0]):
        locations = np.array([x[i], y[i]]).T
        velocities = np.array([vx[i], vy[i]]).T

        energy[i,] = energy_values(G, M, locations, velocities)
    # energy = pd.DataFrame(energy, columns = ["potential_energy", "kinetic_energy", "system_energy"])
    plt.figure()
    plt.violinplot(energy)
    plt.boxplot(energy)
    plt.show()

    plt.figure()
    plt.plot(energy.T[0])
    plt.plot(energy.T[1])
    plt.plot(energy.T[2])
    plt.legend(["potential_energy", "kinetic_energy", "system_energy"])
    plt.savefig(f'energy_plots.svg', format='svg', dpi=1200)
    plt.show()

    Three_body_2D_Rick.plot(x, y)
