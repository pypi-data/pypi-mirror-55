"""
helper_functions.py
----------------------------
Written by C. Lockhart in Python3

A helper function to create a machine learning model engine from a string.
"""

from .logistic import LogisticRegression


# Create machine learning model engine from string
def create_engine_from_string(identifier):
    """
    Create a machine learning model engine from a string.

    Parameters
    ----------
    identifier : str
        String identifier of engine

    Returns
    -------
    engine : object
        An instance of an izzy model class.
    """

    # Type check
    assert isinstance(identifier, str), 'identifier must be string'

    # Convert to lowercase for simplicity and strip and white space
    identifier = identifier.lower().replace(' ', '')

    # Create engine (There needs to be a default; what should this be?)
    engine = None
    if identifier in ('lr', 'logisticregression', 'logit'):
        engine = LogisticRegression(penalty='none', solver='lbfgs', class_weight='balanced', warm_start=False)

    # Return
    return engine


# Determines if `engine` is an instance of an izzy model instance
def is_model_instance(engine):
    """
    Determines if `engine` is an instance of an izzy model instance.

    Parameters
    ----------
    engine : object
        An izzy model instance.

    Returns
    -------
    result : bool
        True or False if engine is an izzy instance.
    """

    # Result True if engine is an object that is linked to izzy package
    return isinstance(engine, object) & (getattr(engine, '_package', None) == 'izzy')


