import math
import os
import time
import numpy as np
from Three_body_2D_Rick import Config, plot, compute_euler, compute_verlet

rf = 1


def initialize_and_save_config() -> Config:
    # initialize configuration
    config: Config = Config(
        name="test_set_3",
        step_size=0.00001,
        range=(0, 2.5),
        iterations=10000,
    )

    config.save()

    return config


def runSimulation(config, init="random", rf=0, noFail=False):
    # initialize x, y, velocity and acceleration vectors
    time_steps = config.time_vector().shape[0]
    x = np.zeros((time_steps, 3), dtype=np.longdouble)
    y = np.zeros((time_steps, 3), dtype=np.longdouble)
    vx = np.zeros((time_steps, 3), dtype=np.longdouble)
    vy = np.zeros((time_steps, 3), dtype=np.longdouble)
    ax = np.zeros((3, 3), dtype=np.longdouble)
    ay = np.zeros((3, 3), dtype=np.longdouble)

    def init_bodies():
        x[0, 0], x[0, 1], x[0, 2] = config.initial_x
        y[0, 0], y[0, 1], y[0, 2] = config.initial_y

        vx[0, 0], vx[0, 1], vx[0, 2] = config.initial_vx
        vy[0, 0], vy[0, 1], vy[0, 2] = config.initial_vy

    def init_next_continuous_iteration():
        config.range = (config.range[1], config.range[1] + increment)

        # reinitialize the lists, with the last value of previous iteration as the first value of the next.
        x[0, 0:3] = x[-1, -3:]
        y[0, 0:3] = y[-1, -3:]
        vx[0, 0:3] = vx[-1, -3:]
        vy[0, 0:3] = vy[-1, -3:]
        ax[0, 0:3] = ax[-1, -3:]
        ay[0, 0:3] = ay[-1, -3:]

    def init_next_random_iteration(x, y, vx, vy, ax, ay):
        # procedure followed by breen et al. (figure 1)
        x1 = 1
        y1 = 0

        x2 = -0.5 + 0.5 * np.random.random()
        y2_max = math.cos(x2)
        y2 = 0 + y2_max * np.random.random()

        x3 = -x1 - x2
        y3 = -y2

        x[0, 0], x[0, 1], x[0, 2] = x1, x2, x3
        y[0, 0], y[0, 1], y[0, 2] = y1, y2, y3

        vx[0, 0:3] = [0, 0, 0]
        vy[0, 0:3] = [0, 0, 0]

        ax[0, 0:3] = [0, 0, 0]
        ay[0, 0:3] = [0, 0, 0]

    def init_special_system():
        x1, y1 = 0, 0
        x2, y2 = -1, 0
        x3, y3 = 1, 0

        vx1, vy1 = 0, 0
        vx2, vy2 = 0, 1
        vx3, vy3 = 0, -1

        x[0, 0], x[0, 1], x[0, 2] = x1, x2, x3
        y[0, 0], y[0, 1], y[0, 2] = y1, y2, y3

        vx[0, 0], vx[0, 1], vx[0, 2] = vx1, vx2, vx3
        vy[0, 0], vy[0, 1], vy[0, 2] = vy1, vy2, vy3

    def init_special_system2():
        x1, y1 = (-0.97000436, 0.24308753)
        x2, y2 = 0, 0
        x3, y3 = (0.97000436, -0.24308753)

        vx1, vy1 = (0.4662036850, 0.4323657300)
        vx2, vy2 = (-0.93240737, -0.86473146)
        vx3, vy3 = vx1, vy1

        x[0, 0], x[0, 1], x[0, 2] = x1, x2, x3
        y[0, 0], y[0, 1], y[0, 2] = y1, y2, y3

        vx[0, 0], vx[0, 1], vx[0, 2] = vx1, vx2, vx3
        vy[0, 0], vy[0, 1], vy[0, 2] = vy1, vy2, vy3

    def save_data(result_id):
        folder = config.get_path() + str(result_id) + "/"

        os.makedirs(folder, exist_ok=True)

        plot(x, y, folder + "plot.svg", show=False)

        np.savez(folder + "data.npz", x=x, y=y, vx=vx, vy=vy)

    if init == "random":
        init_next_random_iteration(x, y, vx, vy, ax, ay)
    elif init == "config":
        init_bodies()
    elif init == "continuous":
        init_next_continuous_iteration
    else:
        raise AssertionError

    increment = config.range[1]
    for iteration in range(rf * config.iterations, (rf + 1) * config.iterations):
        start = time.time()
        moment_of_failure = 0
        while moment_of_failure != -1:

            moment_of_failure = compute_verlet(
                config.time_vector(),
                config.step_size,
                x,
                y,
                config.M,
                ax,
                ay,
                config.G,
                vx,
                vy,
            )

            if moment_of_failure == -1:
                save_data(iteration)
            elif not noFail:
                # runs that failed have only zero's at the end
                # find the point from where everything is all zero's and delete that part of the data
                x = x[:moment_of_failure,]
                y = y[:moment_of_failure,]
                vx = vx[:moment_of_failure,]
                vy = vy[:moment_of_failure,]

                save_data("_" + str(iteration))

            x, y, vx, vy = (
                np.zeros((time_steps, 3), dtype=np.longdouble) for _ in range(4)
            )
            ax, ay = (np.zeros((3, 3), dtype=np.longdouble) for _ in range(2))
            init_next_random_iteration(x, y, vx, vy, ax, ay)

            if not noFail:
                break

        runtime = time.time() - start
        print(f"Run {iteration}: {runtime} seconds")


def main():
    config = initialize_and_save_config()

    runSimulation(config, "random", rf)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Finished in {time.time() - start} seconds")
