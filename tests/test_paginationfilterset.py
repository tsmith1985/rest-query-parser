import pytest

from exceptions import InvalidOperatorException
from filterset import PaginationFilterSet
from operators import EQUAL, GREATER_THAN


pagination_filter_set = PaginationFilterSet(strict=True)


def test_should_parse_valid_limit():
    parsed = pagination_filter_set.parse('limit=10')
    assert any(f['field'] == 'limit' and f['operator'] == EQUAL and f['value'] == 10
               for f in parsed)


def test_should_parse_valid_offset():
    parsed = pagination_filter_set.parse('offset=10')
    assert any(f['field'] == 'offset' and f['operator'] == EQUAL and f['value'] == 10
               for f in parsed)


def test_should_parse_valid_pagination_filters():
    parsed = pagination_filter_set.parse('offset=20&limit=10')
    assert any(f['field'] == 'offset' and f['operator'] == EQUAL and f['value'] == 20
               for f in parsed)
    assert any(f['field'] == 'limit' and f['operator'] == EQUAL and f['value'] == 10
               for f in parsed)


def test_should_raise_error_if_invalid_operator_passed():
    with pytest.raises(InvalidOperatorException):
        pagination_filter_set.parse(f'offset={GREATER_THAN}:20&limit={GREATER_THAN}:10')
    
