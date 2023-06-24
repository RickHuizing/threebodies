import numpy as np
from matplotlib import pyplot as plt

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


def main():
    testResult = "results/default/3/"

    x = np.fromfile(testResult + "x.dat")
    y = np.fromfile(testResult + "y.dat")

    x = x.reshape((x.size//3, 3))
    y = y.reshape((y.size // 3, 3))

    plot(x, y)


if __name__ == "__main__":
    main()