"""
Utilities to check methods and models.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2019

import numbers


def check_ab_method(method, method_options, variant, lift=0,
                    interval_length=0.9):
    """
    Check parameters of A/B testing method.

    Parameters
    ----------
    method : str
        The default computational method.

    method_options : list or tuple
        The list of supported computational methods.

    variant : str
        The chosen variant. Options are "A", "B", "all"

    lift : float (default=0.0)
        The amount of uplift.
    """
    if method not in method_options:
        raise ValueError("Method '{}' is not a valid method. "
                         "Available methods are {}."
                         .format(method, method_options))

    if variant not in ("A", "B", "all"):
        raise ValueError("Variant must be 'A', 'B' or 'all'.")

    if not isinstance(lift, numbers.Number) or lift < 0:
        raise ValueError("Lift must be a positive number;"
                         " got lift={}".format(lift))

    if lift > 0 and method != "MC":
        raise ValueError("Method {} cannot be used with lift={}."
                         " Select method='MC'.".format(method, lift))

    if not isinstance(interval_length, numbers.Number) or (
            interval_length < 0 or interval_length > 1):
        raise ValueError("Interval length must a value in [0, 1]; got "
                         "interval_length={}.".format(interval_length))


def check_mv_method(method, method_options, control, variant, variants, lift=0,
                    interval_length=0.9):
    """
    Check parameters of Multivariate testing method.

    Parameters
    ----------
    method : str
        The default computational method.

    method_options : list or tuple
        The list of supported computational methods.

    control : str
        The control variant.

    variant : str
        The variation variant.

    variants : list or tuple
        The list of available variants.

    lift : float (default=0.0)
        The amount of uplift.
    """
    if method not in method_options:
        raise ValueError("Method '{}' is not a valid method. "
                         "Available methods are {}."
                         .format(method, method_options))

    if control is not None:
        if control not in variants:
            raise ValueError("Control variant '{}' not available. "
                             "Variants = {}.".format(control, variants))

    if variant not in variants:
        raise ValueError("Variant '{}' not available. "
                         "Variants = {}.".format(variant, variants))

    if not isinstance(lift, numbers.Number) or lift < 0:
        raise ValueError("Lift must be a positive number;"
                         " got lift={}.".format(lift))

    if lift > 0 and method != "MC":
        raise ValueError("Method {} cannot be used with lift={}."
                         " Select method='MC'.".format(method, lift))

    if not isinstance(interval_length, numbers.Number) or (
            interval_length < 0 or interval_length > 1):
        raise ValueError("Interval length must a value in [0, 1]; got "
                         "interval_length={}.".format(interval_length))


def check_models(refclass, *models):
    """
    Check that models for A/B and multivariate testing belong to the correct
    class.

    Parameters
    ----------
    refclass : object
        Reference class.

    models : objects
        Model instances to be checked.
    """
    for model_id, model in enumerate(models):
        if not isinstance(model, refclass):
            raise TypeError("Model {} is not an instance of {}."
                            .format(model_id, refclass.__name__))


def check_mv_models(refclass, models):
    """
    Check models for Multivariate testing.

    Parameters
    ----------
    refclass : object
        Reference class.

    models : dict
        Dictionary of model instances to be checked.
    """
    if not isinstance(models, dict):
        raise TypeError("Input models must be of type dict.")

    variants = models.keys()
    variant_control = "A"

    if variant_control not in variants:
        raise ValueError("A model variant 'A' (control) is required.")

    model_classes = models.values()
    check_models(refclass, *model_classes)
