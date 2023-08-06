"""Random vectors generator."""
import numpy as np


def uniform_vectors(size, dim, start=0, stop=1):
    """Generate random vectors with entries from a uniform distribution.

    Parameters
    ----------
    size : int
        The number of vectors to produce.
    dim : int
        The vectors dimension.
    start : float
        Start value of the uniform interval.
    stop : float
        End value of the uniform interval.

    Returns
    -------
    vectors : array, shape (dim, size)
        All the random vectors generated as column vectors.

    """
    shape = (dim, size)
    vectors = np.random.uniform(start, stop, size=shape)
    return vectors
