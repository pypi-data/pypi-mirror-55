"""
metrics.py
----------

Note: this file must be model-agnostic and cannot reference specific model classes.
"""

from scipy.stats import ks_2samp
from sklearn.metrics import roc_auc_score

import numpy as np
import pandas as pd


# Get tp, tn, fp, fn
def _get_tp_tn_fp_fn(y_true, y_pred, threshold=0.5):
    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred, threshold=threshold)

    # We only know how to do this when we have 2 classes
    assert len(cm.columns) == 2

    # Result
    result = {
        'tp': cm.loc[1, 1],
        'tn': cm.loc[0, 0],
        'fp': cm.loc[0, 1],
        'fn': cm.loc[1, 0]
    }

    # Return
    return result


# Accuracy computed from confusion matrix
def _accuracy(tp, tn, fp, fn):
    return (tp + tn) / (tp + tn + fp + fn)


# Accuracy
def accuracy(y_true, y_pred):
    return _accuracy(*confusion_matrix(y_true, y_pred))


# Area under ROC curve
def auroc(y_true, y_pred):
    """
    Computes the area under the Receiver Operator Characteristic curve.

    Parameters
    ----------
    y_true : array-like
        True outcomes.
    y_pred : array-like
        Predicted outcomes

    Returns
    -------
    float
    """

    # Return area under ROC curve
    return roc_auc_score(y_true, y_pred)


# Compute confusion matrix
# TODO allow sample_weight, class_weight
def confusion_matrix(y_true, y_pred, threshold=0.5, sample_weight=None, class_weight=None):
    # Turn y_pred into class
    # TODO this will probably break for multiclass
    y_pred = np.array(y_pred >= threshold, dtype='float')

    # Classes
    classes = np.unique(y_true)

    # Create DataFrame to store results
    cm = pd.DataFrame(index=classes, columns=classes).fillna(0)

    # Will this be too slow? A more Pythonic way would be to use coo_matrix from SciPy (or to use sklearn)
    # TODO make this more efficient
    for class1 in classes:
        for class2 in classes:
            cm.loc[class1, class2] = (np.logical_and(np.equal(y_true, class1), np.equal(y_pred, class2))).sum()

    # Return
    return cm


def _f1(tp, fp, fn, **kwargs):
    return 2. * tp / (2 * tp + fp + fn)


# f1-score
def f1(y_true, y_pred):
    return _f1(*confusion_matrix(y_true, y_pred))


# Compute GINI
def gini(y_true, y_pred):
    """

    Parameters
    ----------
    y_true
    y_pred

    Returns
    -------

    """

    # Return GINI
    return 2. * auroc(y_true, y_pred) - 1.


# KS statistic
# TODO will this work in a multiclass scenario?
def ks(y_true, y_pred):
    """
    Computes the KS statistic.

    Parameters
    ----------
    y_true : array-like
        True y values
    y_pred : array-like
        Predicted y values.

    Returns
    -------
    KS statistic : float
    """

    # Compute KS statistic
    statistic, p_value = ks_2samp(y_pred[y_true == 0], y_pred[y_true == 1])

    # Return KS statistic
    return statistic


def _precision(tp, fp, **kwargs):
    return tp / (tp + fp)


def precision(y_true, y_pred):
    return _precision(*confusion_matrix(y_true, y_pred))


def _recall(tp, fn, **kwargs):
    return tp / (tp + fn)


def recall(y_true, y_pred):
    return _recall(*confusion_matrix(y_true, y_pred))


# Generate model performance report
def performance(y_true, y_pred, threshold=0.5):
    """

    Parameters
    ----------
    y_true : array-like
        True outcomes.
    y_pred : array-like
        Predicted outcomes.

    Returns
    -------

    """

    # Empty report container
    r = pd.Series()

    # Accuracy, precision, recall, f1
    cm = _get_tp_tn_fp_fn(y_true, y_pred, threshold=threshold)
    r['accuracy'] = _accuracy(**cm)
    r['precision'] = _precision(**cm)
    r['recall'] = _recall(**cm)
    r['f1'] = _f1(**cm)

    # KS statistic
    r['KS'] = ks(y_true, y_pred)

    # AUROC / GINI
    r['AUROC'] = auroc(y_true, y_pred)
    r['GINI'] = gini(y_true, y_pred)

    # TODO slope

    # TODO correlation

    # Return report
    return r
