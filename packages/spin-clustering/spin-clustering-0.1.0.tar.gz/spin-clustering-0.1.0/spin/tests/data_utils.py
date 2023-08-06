"""Auxiliar functions to support the SPIN test suit."""
import numpy as np


def generate_2d_data(points_per_cluster, n_clusters):
    """Generate simple clusters in the plane.

    Parameters
    ----------
    points_per_cluster : int
        The amount of points for each cluster.
    n_clusters : int
        The number of clusters to generate.

    Returns
    -------
    points : array, shape (2, points_per_cluster * n_clusters)

    """
    cluster_points = []
    for i in range(n_clusters):
        center = (np.random.uniform(0, 4), np.random.uniform(0, 4))
        std = np.random.uniform(0, 0.1, 1)
        cov_matrix = [[std, 0], [0, std]]
        points = np.random.multivariate_normal(center,
                                               cov_matrix,
                                               points_per_cluster).T
        cluster_points.append(points)

    points = np.concatenate(cluster_points, axis=1)
    index = [i for i in range(points.shape[1])]
    np.random.shuffle(index)
    points = points[:, index]
    return points
