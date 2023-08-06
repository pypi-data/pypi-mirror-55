"""
generic.py
----------

Contains the GenericModel parent class
"""

from .metrics import confusion_matrix, performance


# GenericModel class
class GenericModel:
    """
    GenericModel class. Note that this class is not meant to be directly used.
    """

    # Initialize instance of class
    def __init__(self):
        """
        Initialize instance of the GenericModel class. Note that this class is not meant to be directly used.
        """

        raise NotImplementedError('do not directly create a GenericModel instance')

    # Confusion matrix
    def confusion_matrix(self, x, y):
        # Predicted y
        y_pred = self.predict_y(x)

        # Return
        return confusion_matrix(y, y_pred)

    # Fit the model
    def fit(self, *args, **kwargs):
        """
        Fit the model.
        """

        raise NotImplementedError('do not directly used GenericModel class')

    # predict_y placeholder
    def predict_y(self, x):
        """
        This method is a placeholder and not meant to be directly used.

        Parameters
        ----------
        x : array-like
            The independent variable.
        """

        raise NotImplementedError('this method is not meant to be used')

    # Generate performance report
    def performance(self, x, y):
        """

        Parameters
        ----------
        x : array-like
            The independent variables.
        y : array-like
            The dependent variables.

        Returns
        -------
        pandas Series
        """

        # Get predicted y values from model
        y_pred = self.predict_y(x)

        # Return performance report
        return performance(y, y_pred)
