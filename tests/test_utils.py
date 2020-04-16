from constants import EMPTY_VALUES
from utils import coalesce


def test_coalesce_should_return_first_non_empty_value():
    result = coalesce(*EMPTY_VALUES, 1)
    assert result == 1


def test_coalesce_should_return_none_if_no_non_empty_values():
    result = coalesce(*EMPTY_VALUES)
    assert result is None
