"""Reimplementation of isclose for older Python versions."""

from math import isinf


def isclose(number_a, number_b, rel_tol=1e-9, abs_tol=0.0):
    """
    Determine whether two floating point numbers are close in value.

    rel_tol:
        maximum difference for being considered "close", relative to
        the magnitude of the input values
    abs_tol:
        maximum difference for being considered "close", regardless
        of the magnitude of the input values

    Determine whether two floating point numbers are close in value.

    Return True if a is close in value to b, and False otherwise.

    For the values to be considered close, the difference between
    them must be smaller than at least one of the tolerances.

    -inf, inf and NaN behave similarly to the IEEE 754 Standard. That
    is, NaN is not close to anything, even itself.  inf and -inf are
    only close to themselves.
    """
    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('tolerances must be non-negative')

    if number_a == number_b:
        return True

    if isinf(number_a) or isinf(number_b):
        return False

    # Convert to float here because comparing floats and Decimals is
    # arbitrary before Python 2.7.
    number_a_float = float(number_a)
    number_b_float = float(number_b)

    diff = abs(number_b_float - number_a_float)

    return (
        (
            (diff <= abs(rel_tol * number_b_float)) or
            (diff <= abs(rel_tol * number_a_float))
        ) or
        (diff <= abs_tol)
    )
