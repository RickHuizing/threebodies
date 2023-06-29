from dataclasses import dataclass, field
from typing import List

import numpy as np
from dataclasses_json import DataClassJsonMixin
from matplotlib import pyplot as plt
import matplotlib_style

matplotlib_style.init_plt_style()


def compute_a(x, y, M, ax, ay, G):
    for j in range(3):
        # Compute the distance between current body and the others(also with itself )
        dx = (x[j] - x).T.conj()
        dy = (y[j] - y).T.conj()

        # Compute the acceleration according to Newton law
        ax[:, j] = ((-dx) * M * G) / (np.sqrt(dx ** 2 + dy ** 2) ** 3)
        ay[:, j] = ((-dy) * M * G) / (np.sqrt(dx ** 2 + dy ** 2) ** 3)

        np.nan_to_num(ax, False, 0)
        np.nan_to_num(ay, False, 0)

    return np.sum(ax, axis=0), np.sum(ay, axis=0)


def compute_euler(time_steps, step_size, x, y, M, ax, ay, G, vx, vy):
    # simple euler method
    for i in range(time_steps.size - 1):
        # Compute current acceleration
        ax_tot, ay_tot = compute_a(x[i, :], y[i, :], M, ax, ay, G)

        # Update the position
        nx = x[i, :] + step_size * vx[i, :]
        ny = y[i, :] + step_size * vy[i, :]
        x[i + 1, :] = nx
        y[i + 1, :] = ny

        # update the velocity
        vx[i + 1, :] = vx[i, :] + step_size * ax_tot
        vy[i + 1, :] = vy[i, :] + step_size * ay_tot

        # failure - bodies too far apart
        if np.max(nx) > 3 or np.max(ny) > 3 or np.min(nx) < -3 or np.min(ny) < -3:
            return i + 1

    return -1  # success


def compute_verlet(time_steps, step_size, x, y, M, ax, ay, G, vx, vy):
    half_step_size_sq = 0.5 * (step_size ** 2)
    half_step_size = 0.5 * step_size
    for i in range(x.shape[0] - 1):
        # Compute current acceleration
        ax_tot, ay_tot = compute_a(x[i, :], y[i, :], M, ax, ay, G)

        # Update the position
        nx = x[i, :] + step_size * vx[i, :] + half_step_size_sq * ax_tot
        ny = y[i, :] + step_size * vy[i, :] + half_step_size_sq * ay_tot

        # early stop - bodies too far apart
        if np.max(nx) > 3 or np.max(ny) > 3 or np.min(nx) < -3 or np.min(ny) < -3:
            return i + 1

        x[i + 1, :] = nx
        y[i + 1, :] = ny

        # Compute the next time acceleration
        ax_tot_next, ay_tot_next = compute_a(x[i + 1, :], y[i + 1, :], M, ax, ay, G)

        # Compute the next time velocity according to the Verlet method
        vx[i + 1, :] = vx[i, :] + half_step_size * (ax_tot + ax_tot_next)
        vy[i + 1, :] = vy[i, :] + half_step_size * (ay_tot + ay_tot_next)

    return -1  # success


def plot(x, y, path: str = None, show=True, savefig=True):
    if not show and not savefig:
        return

    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    plt.title("Simple Euler method")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim((-3, 3))
    plt.ylim((-3, 3))
    # plt.xscale("logit")
    # plt.yscale("logit")
    plt.plot(x[:, 0], y[:, 0], 'r')
    plt.plot(x[:, 1], y[:, 1], 'g')
    plt.plot(x[:, 2], y[:, 2], 'b')
    plt.plot(x[0, 0], y[0, 0], 'ro')
    plt.plot(x[0, 1], y[0, 1], 'go')
    plt.plot(x[0, 2], y[0, 2], 'bo')

    plt.legend(('Body 1', 'Body 2', 'Body 3'))

    if savefig and path is not None:
        plt.savefig(path)
    if show:
        plt.show()


@dataclass()
class Config(DataClassJsonMixin):
    # name of the configuration, used as folder name while saving results
    name: str = "default"

    # time parameters. Default is from t0 to t5, with steps of 0.001. Result is a dataset of 5000 time steps
    range: tuple = (0, 5)
    step_size: float = 0.001

    # iterations
    iterations: int = 10

    # body mass
    m1: np.longdouble = 1
    m2: np.longdouble = 1
    m3: np.longdouble = 1

    # Newton constant
    G: np.longdouble = 1

    # initial locations
    initial_x: List = field(default_factory=lambda: [0, 0, 0])
    initial_y: List = field(default_factory=lambda: [1, -1, 0])

    # initial velocities
    initial_vx: List = field(default_factory=lambda: [0.3471, 0.3471, -2 * 0.3471])
    initial_vy: List = field(default_factory=lambda: [0.5327, 0.5327, -2 * 0.5327])

    # body mass
    M = np.array([m1, m2, m3])

    def time_vector(self):
        return np.arange(*self.range, self.step_size)

    def get_path(self):
        return "results/{0}/".format(self.name)
