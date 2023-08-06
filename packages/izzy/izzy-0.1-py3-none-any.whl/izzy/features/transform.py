"""
transform.py
------------


"""

from izzy.regression import sigmoid_fit

import numpy as np
import pandas as pd


# Clip
def clip(array, left=None, right=None, cut=False):
    """
    Clip the array. If cut = False, this sets any values < left to left and values > right to right.
    If cut = True, then the values < left and values > right are removed.

    Parameters
    ----------
    array : array-like
        The array to clip.
    left : scalar
        The left boundary to clip / cut.
    right : scalar
        The right boundary to clip / cut.
    cut : bool
        Flag to determine if we should clip / cut.

    Returns
    -------
    array
    """

    # If cut = False, use numpy clip function
    if not cut:
        array = np.clip(array, a_min=left, a_max=right)

    # Otherwise, cut
    else:
        x = array >= left
        y = array <= right
        array = array[x & y]

    # Return array
    return array


# Desigmoid
def desigmoid(x, y, a=None, n=None):
    # Get sigmoid optimized parameters
    if a is None or n is None:
        a, n = sigmoid_fit(x, y)

    # Return inverse of sigmoid
    return np.power((1. - x) / (a * x), 1./n)


# Granulate
def granulate(array, bins=None, mode=None, retbins=False):
    """
    Take an array,

    Parameters
    ----------
    array : array-like

    bins : int or array-like

    mode : str
        Options include 'quantile', 'equal', 'left-equal', 'right-equal', 'binary', or 'distinct'. Note that 'equal' and
        'left-equal' are synonyms. If mode = 'distinct', no transformation is performed. The mode = 'binary' is the same
         as 'distinct', except that we check that there are only two types of observations.

    retbins : bool

    Returns
    -------
    array

    """

    # Alias mode = 'equal' to 'left-equal'
    if mode == 'equal':
        mode = 'left-equal'

    # Minimum and maximum of array
    array_min = np.min(array)
    array_max = np.max(array)

    # Assign labels for equal bin sizes using numpy.digitize
    if mode in ('left-equal', 'right-equal'):
        # Is bins an integer? If so, we need to generate
        if isinstance(bins, np.int):
            # Inflate boundaries of minimum and maximum to cover all values
            array_min_inflated = array_min - 0.01 * np.abs(array_min)
            array_max_inflated = array_max + 0.01 * np.abs(array_max)

            # Create bins
            # bins = np.linspace(start=array_min_inflated, stop=array_max_inflated, num=bins + 1)
            bins = np.linspace(start=array_min, stop=array_max, num=bins + 1)

            # If left-equal, set last bin to infinity. If right-equal, set first bin to -infinity.
            if mode == 'left-equal':
                bins[-1] = np.inf
            elif mode == 'right-equal':
                bins[0] = -np.inf

        # Are these bins right-aligned?
        right = False if mode == 'left-equal' else True

        # Transform array
        array = np.digitize(array, bins=bins, right=right)

    # Assign labels for quantiles
    elif mode == 'quantile':
        array, _ = pd.qcut(x=array, q=bins, labels=False, retbins=True, duplicates='drop')

    # If binary, check that there are only two types of observations
    elif mode == 'binary':
        assert len(np.unique(array)) == 2, 'expecting only two types of observations'

    # Return
    result = array
    if retbins:
        result = (result, bins)
    return result


# Natural logarithm
def ln(array):
    return log(array)


# Logarithm for arbitrary base
def log(array, base=10):
    return np.log(array) / np.log(base)


# Raise to arbitrary power
def power(array, exponent):
    return np.power(array, exponent)


# Square
def square(array):
    return power(array, exponent=2)
