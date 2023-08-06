"""
LogisticRegression.py
---------------------
Written by C. Lockhart in Python3
"""

from .generic import GenericModel

from sklearn.linear_model import LogisticRegression as _LogisticRegression


# LogisticRegression class
class LogisticRegression(_LogisticRegression, GenericModel):
    """
    LogisticRegression class, child of sklearn.linear_model.LogisticRegression
    """

    # Initialize class instance
    def __init__(self, **kwargs):
        """
        Initialize an instance of LogisticRegression

        Calls parent class from sklearn.linear_model.LogisiticRegression
        """

        # Initialize parent class
        _LogisticRegression.__init__(self, **kwargs)

        # Set package reference
        self._package = 'izzy'

    # Confusion matrix
    def confusion_matrix(self, x, y):
        return GenericModel.confusion_matrix(self, x, y)

    # Feature importance
    # TODO encode this method
    def feature_importance(self):
        pass

    # Predict the outcome
    def predict_y(self, x):
        """
        Returns the predict outcomes from the model.

        Parameters
        ----------
        x : array-like
            Input variables

        Returns
        -------
        y : array
            The predicted outcomes.
        """

        # Return
        return self.predict_proba(x)[:, 1]

    # Performance report
    def performance(self, x, y):
        """

        Parameters
        ----------
        x
        y

        Returns
        -------

        """

        return GenericModel.performance(self, x, y)
