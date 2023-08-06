"""
impute.py

Examples
--------
>>> from izzy.features import Imputer
>>> im = Imputer(special_values=['A', 'B', np.nan], mode='fill', values=5)
>>> x_imputed = im.transform(X)


Imput
>>> from izzy.dataset import random_dataset
>>> df = random_dataset()
>>> df.impute()

"""

import numpy as np
import pandas as pd


# A class for imputing missing values
class Imputer:
    """
    Replace missing values in a dataset.
    """

    # Initialize class instance
    def __init__(self, missing_values=None, mode='fill', **kwargs):
        """

        Parameters
        ----------
        missing_values : list
            Values that need imputation.

        """

        # Values that need to be imputed
        self.missing_values = missing_values if missing_values is not None else [np.nan]

        # Mode
        self.mode = '_' + mode.lower()
        self.kwargs = kwargs

    # Fill array-like structure
    # TODO add ability to parallelize these processes (maybe by using ray.dataframe?)
    def _fill(self, data, fill_value=0):
        # If fill_value is a dictionary, the keys represent data columns
        if isinstance(fill_value, dict):
            for key, value in fill_value.items():
                if isinstance(data, pd.DataFrame):
                    data[key] = self._fill(data[key], value)
                elif isinstance(data, pd.Series):
                    raise AttributeError('unable to apply dict fill_value to Series')
                else:
                    data[:, key] = self._fill(data[:, key], value)

        # Else if fill_value is a list, the list items represent tuples of missing_values and their fills
        elif isinstance(fill_value, list):
            for value in fill_value:
                data = self._fill(data, value)

        # Else if tuple, the first value is the missing_value and the second value is the fill
        elif isinstance(fill_value, tuple):
            key, value = fill_value
            if isinstance(data, pd.DataFrame):
                data.loc[data == key, :] = value
            else:
                data[data == key] = value

        # Else, singular
        else:
            if isinstance(data, pd.DataFrame):
                data.loc[data.isin(self.missing_values), :] = fill_value
            elif isinstance(data, pd.Series):
                data[data.isin(self.missing_values)] = fill_value
            else:
                data[data in self.missing_values] = fill_value

        # Return
        return data

    # WOE interpolation
    # TODO write out this function
    def _woe(self, data, ):
        pass

    # Transform the data
    def transform(self, data):
        """
        Actually transform the data.

        Parameters
        ----------
        data : array-like

        Returns
        -------

        """

        # Get mode
        mode = self.mode

        # Run function
        getattr(self, mode)(**self.kwargs)


# Impute for a single
def impute(x, y, method='woe', **kwargs):
    # Create an Imputer instance
    pass
