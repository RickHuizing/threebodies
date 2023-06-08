import numpy as np

"""
CALCULATIONS FOUND IN https://fse.studenttheses.ub.rug.nl/8656/1/Math_Drs_1998_BOldeman.CV.pdf
"""


def energy_values(G: float, M: np.ndarray, locations: np.ndarray, velocities: np.ndarray):
    potential_energy = calculate_potential_energy(G, M, locations)
    kinetic_energy = calculate_kinetic_energy(M, velocities)
    return potential_energy, kinetic_energy, potential_energy + kinetic_energy


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
