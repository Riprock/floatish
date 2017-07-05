"""Tests for floatish."""

from floatish import Floatish


def test_floatish_basic():
    """Test Floatish works for the common example and default args."""
    assert 0.2 + 0.1 == Floatish(0.3)


def test_floatish_left():
    """Test Floatish works the same if used on the left of an ==."""
    assert Floatish(0.3) == 0.2 + 0.1


def test_floatish_low_tolerance():
    """Test Floatish returns False if relative tolerance still too small."""
    assert 0.2 + 0.1 != Floatish(0.3, rel_tol=1e-16)


def test_floatish_abs_close():
    """Test floatish handles absolute tolerance correctly."""
    assert Floatish(0.3, abs_tol=0.1) == 0.291


def test_floatish_abs_not_close():
    """Test floatish handles lower absolute tolerance correctly."""
    assert Floatish(0.3, abs_tol=0.005) != 0.291


def test_two_floatish():
    """Test comparing two Floatish doesn't blow up."""
    assert Floatish(0.3) == Floatish(0.3)


def test_two_floatish_true():
    """Test comparing two Floatish if both sides are different yet True."""
    assert Floatish(0.25, abs_tol=0.05) == Floatish(0.259, abs_tol=0.01)


def test_two_floatish_false():
    """Test comparing two Floatish is False if one side is False."""
    assert Floatish(0.28, abs_tol=0.05) != Floatish(0.259, abs_tol=0.01)
