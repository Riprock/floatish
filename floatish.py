"""Floatish can be used to compare floats, even inside a collection."""

try:
    from math import isclose
except ImportError:
    from floatishisclose import isclose


class Floatish(object):
    """
    Will be equal to floats that are close.

    After making a new instance you can inspect the value, abs_tol, and
    rel_tol attributes.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, value, abs_tol=None, rel_tol=None):
        """
        Set the value to compare and the tolerances.

        abs_tol and rel_tol have the same meaning as for math.isclose.
        None means not to pass the arg, causing the default for isclose
        to be used.
        """
        self.value = value
        self.abs_tol = abs_tol
        self.rel_tol = rel_tol

    def __eq__(self, other):
        """
        Return if isclose or defer.

        If comparing two Floatish, only return True if both conditions
        are true.
        """
        if isinstance(other, float):
            isclose_kwargs = {}
            if self.rel_tol is not None:
                isclose_kwargs['rel_tol'] = self.rel_tol
            if self.abs_tol is not None:
                isclose_kwargs['abs_tol'] = self.abs_tol
            return isclose(self.value, other, **isclose_kwargs)
        elif isinstance(other, Floatish):
            return self == other.value and self.value == other
        return NotImplemented
