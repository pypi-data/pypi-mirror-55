import pytest as pt
import numpy as np

from ..distances import l2_distance_matrix
from .random_vectors import uniform_vectors

RANDOM_TEST_SIZE = 200


class TestL2DistanceMatrix:

    random_test_sample_diagonal = np.random.randint(
            0,
            100,
            size=(RANDOM_TEST_SIZE, 2)
            )

    @pt.mark.parametrize("n_vectors,dim",
                         random_test_sample_diagonal)
    def test_diagonal_multiple_random_vectors(self, n_vectors, dim):
        vectors = uniform_vectors(n_vectors, dim)
        distances = l2_distance_matrix(vectors, vectors)
        assert distances.shape == (n_vectors, n_vectors)
        assert np.allclose(distances, distances.T)
        assert distances.diagonal().sum() < 1e-5
