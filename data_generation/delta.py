import numpy as np


def get_deltas(x: np.ndarray, y: np.ndarray, vx: np.ndarray, vy: np.ndarray, delta=1, scaling_factor=1):
    dx = (x[:-delta] - x[delta:]) * scaling_factor
    dy = (y[:-delta] - y[delta:]) * scaling_factor
    dvx = (vx[:-delta] - vx[delta:]) * scaling_factor
    dvy = (vy[:-delta] - vy[delta:]) * scaling_factor
    return dx, dy, dvx, dvy


def reverse_deltas(previous_state: np.ndarray, prediction: np.ndarray, scaling_factor):
    return previous_state - (prediction / scaling_factor)
