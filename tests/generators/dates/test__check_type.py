import pytest


import pytest
from generators.dates import _check_type


def test__check_type():
    with pytest.raises(
        TypeError, match=r"5 is expected to be 'float'\. Instead got a value of 5 \('int'\)"
    ):
        _check_type(5, "5", float)

    with pytest.raises(
        TypeError, match=r"5 is expected to be one of \('float',\)\. Instead got a value of 5 \('int'\)"
    ):
        _check_type(5, "5", (float,))

    with pytest.raises(
        TypeError,
        match=r"5 is expected to be one of \('float', 'str'\)\. Instead got a value of 5 \('int'\)",
    ):
        _check_type(5, "5", (float, str))

    assert _check_type(5, "5", int) is None
    assert _check_type(5, "5", (int,)) is None
    assert _check_type(5, "5", (int, float)) is None
