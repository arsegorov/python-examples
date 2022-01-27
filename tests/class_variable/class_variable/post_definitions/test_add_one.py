from class_variable.post_definition import PostdefinedVariable
from hypothesis import given, strategies as st


@given(st.integers())
def test_add_one(n):
    assert PostdefinedVariable.add_one(n) == n + 1
