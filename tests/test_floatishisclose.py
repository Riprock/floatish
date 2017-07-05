"""
Tests for floatishisclose.

Copied from the standard library tests for isclose and made prettier for
pytest.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from floatishisclose import isclose


def test_negative_tolerances_rel():
    """Test ValueError raised if relative tolerance is less than zero."""
    with pytest.raises(ValueError):
        isclose(1, 1, rel_tol=-1e-100)


def test_negative_tolerances_both():
    """Test ValueError raised if either tolerance is less than zero."""
    with pytest.raises(ValueError):
        isclose(1, 1, rel_tol=1e-100, abs_tol=-1e10)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (2.0, 2.0),
        (0.1e200, 0.1e200),
        (1.123e-300, 1.123e-300),
        (12345, 12345.0),
        (0.0, -0.0),
        (345678, 345678),
    ]
)
def test_identical(number_a, number_b):
    """Test identical values are close."""
    assert isclose(number_a, number_b, rel_tol=0.0, abs_tol=0.0)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (1e8, 1e8 + 1),
        (-1e-8, -1.000000009e-8),
        (1.12345678, 1.12345679),
    ]
)
def test_eight_decimal_places_8(number_a, number_b):
    """Test numbers within 1e-8 relative are close."""
    assert isclose(number_a, number_b, rel_tol=1e-8)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (1e8, 1e8 + 1),
        (-1e-8, -1.000000009e-8),
        (1.12345678, 1.12345679),
    ]
)
def test_eight_decimal_places_9(number_a, number_b):
    """Test numbers within 1e-8 are not within 1e-9."""
    assert not isclose(number_a, number_b, rel_tol=1e-9)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (1e-9, 0.0),
        (-1e-9, 0.0),
        (-1e-150, 0.0),
    ]
)
def test_near_zero_rel(number_a, number_b):
    """Test values close to zero are not within any relative tolerance."""
    assert not isclose(number_a, number_b, rel_tol=0.9)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (1e-9, 0.0),
        (-1e-9, 0.0),
        (-1e-150, 0.0),
    ]
)
def test_near_zero_abs(number_a, number_b):
    """Test values close to zero are within absolute tolerance 1e-8."""
    assert isclose(number_a, number_b, abs_tol=1e-8)


def test_identical_infinite_pos():
    """Test infinities close."""
    assert isclose(float('inf'), float('inf'))


def test_identical_infinite_pos_abs():
    """Test infinities are close with no absolute tolerance."""
    assert isclose(float('inf'), float('inf'), abs_tol=0.0)


def test_identical_infinite_neg():
    """Test negative infinities are close."""
    assert isclose(float('-inf'), float('-inf'))


def test_identical_infinite_neg_abs():
    """Test negative infinities are close with no absolute tolerance."""
    assert isclose(float('-inf'), float('-inf'), abs_tol=0.0)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (float('nan'), float('nan')),
        (float('nan'), 1e-100),
        (1e-100, float('nan')),
        (float('inf'), float('nan')),
        (float('nan'), float('inf')),
        (float('inf'), float('-inf')),
        (float('inf'), 1.0),
        (1.0, float('inf')),
        (float('inf'), 1e308),
        (1e308, float('inf')),
    ]
)
def test_inf_ninf_nan(number_a, number_b):
    """
    Test examples are never close using largest reasonable tolerance.

    This is by IEEE 754 definition for Nan and infinity.
    """
    assert not isclose(number_a, number_b, abs_tol=0.999999999999999)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (1.0, 1.0),
        (-3.4, -3.4),
        (-1e-300, -1e-300),
    ]
)
def test_zero_tolerance(number_a, number_b):
    """Test identical numbers are close with no relative tolerance."""
    assert isclose(number_a, number_b, rel_tol=0.0)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (1.0, 1.000000000000001),
        (0.99999999999999, 1.0),
        (1.0e200, .999999999999999e200),
    ]
)
def test_zero_tolerance_not(number_a, number_b):
    """Test different numbers aren't close with no relative tolerance."""
    assert not isclose(number_a, number_b, rel_tol=0.0)


@pytest.mark.parametrize('number_a, number_b', [(9, 10), (10, 9)])
def test_asymmetry(number_a, number_b):
    """Test that order of numbers does not matter."""
    assert isclose(number_a, number_b, rel_tol=0.1)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (100000001, 100000000),
        (123456789, 123456788),
    ]
)
def test_integers_8(number_a, number_b):
    """Test integers are close with relative tolerance of 1e-8."""
    assert isclose(number_a, number_b, rel_tol=1e-8)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (100000001, 100000000),
        (123456789, 123456788),
    ]
)
def test_integers_9(number_a, number_b):
    """Test integers are not close with relative tolerance of 1e-9."""
    assert not isclose(number_a, number_b, rel_tol=1e-9)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (Decimal('1.00000001'), Decimal('1.0')),
        (Decimal('1.00000001e-20'), Decimal('1.0e-20')),
        (Decimal('1.00000001e-100'), Decimal('1.0e-100')),
        (Decimal('1.00000001e20'), Decimal('1.0e20')),
    ]
)
def test_decimals_8(number_a, number_b):
    """Test Decimals are close with relative tolerance of 1e-8."""
    assert isclose(number_a, number_b, rel_tol=1e-8)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (Decimal('1.00000001'), Decimal('1.0')),
        (Decimal('1.00000001e-20'), Decimal('1.0e-20')),
        (Decimal('1.00000001e-100'), Decimal('1.0e-100')),
        (Decimal('1.00000001e20'), Decimal('1.0e20')),
    ]
)
def test_decimals_9(number_a, number_b):
    """Test Decimals are not close with relative tolerance of 1e-9."""
    assert not isclose(number_a, number_b, rel_tol=1e-9)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (Fraction(1, 100000000) + 1, Fraction(1)),
        (Fraction(100000001), Fraction(100000000)),
        (Fraction(10**8 + 1, 10**28), Fraction(1, 10**20))
    ]
)
def test_fractions_8(number_a, number_b):
    """Test Fractions are close with relative tolerance of 1e-8."""
    assert isclose(number_a, number_b, rel_tol=1e-8)


@pytest.mark.parametrize(
    'number_a, number_b',
    [
        (Fraction(1, 100000000) + 1, Fraction(1)),
        (Fraction(100000001), Fraction(100000000)),
        (Fraction(10**8 + 1, 10**28), Fraction(1, 10**20))
    ]
)
def test_fractions_9(number_a, number_b):
    """Test Fractions are not close with relative tolerance of 1e-9."""
    assert not isclose(number_a, number_b, rel_tol=1e-9)
