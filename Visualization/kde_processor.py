
import numpy as np
from sklearn.neighbors import KernelDensity

def compute_kde(x_coords, y_coords, bandwidth=200, grid_size=200, bounds=None):
    xy = np.vstack([x_coords, y_coords]).T
    kde = KernelDensity(bandwidth=bandwidth, metric='euclidean').fit(xy)

    x_min, y_min, x_max, y_max = bounds
    x_grid, y_grid = np.meshgrid(np.linspace(x_min, x_max, grid_size), np.linspace(y_min, y_max, grid_size))
    xy_sample = np.vstack([x_grid.ravel(), y_grid.ravel()]).T

    z = np.exp(kde.score_samples(xy_sample)).reshape(x_grid.shape)
    return x_grid, y_grid, z
