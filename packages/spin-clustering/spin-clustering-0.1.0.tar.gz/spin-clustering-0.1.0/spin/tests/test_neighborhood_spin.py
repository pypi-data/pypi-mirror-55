"""Neighborhood SPIN module tests unit."""
import pytest as pt
import numpy as np

from .data_utils import generate_2d_data
from ..neighborhood_spin import NeighborhoodSPIN
from ..distances import l2_distance_matrix


class TestNeighborhoodSPIN():

    simple_exectuion_runs = [
            (10, 10),
            (100, 3),
            (500, 1),
            (50, 4),
            (30, 6),
            (20, 10),
            (200, 2),
            (300, 3),
            ]

    @pt.mark.parametrize("points_per_cluster,n_clusters",
                         simple_exectuion_runs)
    def test_simple_execution(self, points_per_cluster, n_clusters):
        spin = NeighborhoodSPIN()
        data = generate_2d_data(points_per_cluster, n_clusters)
        distances = l2_distance_matrix(data, data)
        spin.run(distances)

    @pt.mark.parametrize("points_per_cluster,n_clusters",
                         simple_exectuion_runs)
    def test_assert_permutation_matrix_produces_ordered_distances(
            self,
            points_per_cluster,
            n_clusters
            ):
        spin = NeighborhoodSPIN()
        data = generate_2d_data(points_per_cluster, n_clusters)
        distances = l2_distance_matrix(data, data)
        spin.run(distances)
        permutation = spin.permutation_
        ordered_distances = permutation.dot(distances).dot(permutation.T)
        assert np.array_equal(ordered_distances, spin.ordered_distances_)
