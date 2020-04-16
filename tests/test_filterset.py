import pytest

from exceptions import (NullNotAllowedException, InvalidBooleanException, InvalidIntegerException,
                        InvalidFloatException)
from filters import BooleanFilter, FloatFilter, IntegerFilter, StringFilter
from filterset import FilterSet
from operators import (EQUAL, NOT_EQUAL, IN, NOT_IN, GREATER_THAN, GREATER_THAN_OR_EQUAL,
                       LESS_THAN, LESS_THAN_OR_EQUAL)


class PersonFilterSet(FilterSet):
    name = StringFilter(allow_null=False)
    age = IntegerFilter()
    weight = FloatFilter()
    divorced = BooleanFilter()


passive_filter_set = PersonFilterSet()
strict_filter_set = PersonFilterSet(strict=True)


# string filter tests
def test_should_parse_valid_string_filter():
    parsed = passive_filter_set.parse('name=Ron Swanson')
    assert any(f['field'] == 'name' and f['operator'] == EQUAL and f['value'] == 'Ron Swanson'
               for f in parsed)


def test_should_parse_valid_string_filter_with_equal_operator():
    parsed = passive_filter_set.parse(f'name={EQUAL}:Ron Swanson')
    assert any(f['field'] == 'name' and f['operator'] == EQUAL and f['value'] == 'Ron Swanson'
               for f in parsed)


def test_should_parse_valid_string_filter_with_not_equal_operator():
    parsed = passive_filter_set.parse(f'name={NOT_EQUAL}:Ron Swanson')
    assert any(f['field'] == 'name' and f['operator'] == NOT_EQUAL and f['value'] == 'Ron Swanson'
               for f in parsed)


def test_should_parse_valid_string_filter_with_in_operator():
    parsed = passive_filter_set.parse(f'name={IN}:Ron Swanson')
    assert any(f['field'] == 'name' and f['operator'] == IN and f['value'] == 'Ron Swanson'
               for f in parsed)


def test_should_parse_valid_string_filter_with_not_in_operator():
    parsed = passive_filter_set.parse(f'name={NOT_IN}:Ron Swanson')
    assert any(f['field'] == 'name' and f['operator'] == NOT_IN and f['value'] == 'Ron Swanson'
               for f in parsed)


def test_should_ignore_if_passive_mode_and_allow_null_is_false():
    parsed = passive_filter_set.parse('name=null')
    assert not parsed


def test_should_raise_error_if_strict_mode_and_allow_null_is_false():
    with pytest.raises(NullNotAllowedException):
        strict_filter_set.parse('name=null')


def test_should_allow_filtering_by_empty_string():
    parsed1 = passive_filter_set.parse('name')
    parsed2 = passive_filter_set.parse('name=')
    assert any(f['field'] == 'name' and f['operator'] == EQUAL and f['value'] == ''
               for f in parsed1)
    assert any(f['field'] == 'name' and f['operator'] == EQUAL and f['value'] == ''
               for f in parsed2)


def test_should_allow_filtering_by_not_empty_string():
    parsed1 = passive_filter_set.parse(f'name={NOT_EQUAL}')
    parsed2 = passive_filter_set.parse(f'name={NOT_EQUAL}:')
    assert any(f['field'] == 'name' and f['operator'] == NOT_EQUAL and f['value'] == ''
               for f in parsed1)
    assert any(f['field'] == 'name' and f['operator'] == NOT_EQUAL and f['value'] == ''
               for f in parsed2)


# integer filter tests
def test_should_parse_valid_integer_filter():
    parsed = passive_filter_set.parse('age=65')
    assert any(f['field'] == 'age' and f['operator'] == EQUAL and f['value'] == 65 for f in parsed)


def test_should_parse_valid_integer_filter_with_equal_operator():
    parsed = passive_filter_set.parse(f'age={EQUAL}:65')
    assert any(f['field'] == 'age' and f['operator'] == EQUAL and f['value'] == 65 for f in parsed)


def test_should_parse_valid_integer_filter_with_not_equal_operator():
    parsed = passive_filter_set.parse(f'age={NOT_EQUAL}:65')
    assert any(f['field'] == 'age' and f['operator'] == NOT_EQUAL and f['value'] == 65 for f in parsed)


def test_should_parse_valid_integer_filter_with_greater_than_operator():
    parsed = passive_filter_set.parse(f'age={GREATER_THAN}:65')
    assert any(f['field'] == 'age' and f['operator'] == GREATER_THAN and f['value'] == 65 for f in parsed)


def test_should_parse_valid_integer_filter_with_greater_than_or_equal_operator():
    parsed = passive_filter_set.parse(f'age={GREATER_THAN_OR_EQUAL}:65')
    assert any(f['field'] == 'age' and f['operator'] == GREATER_THAN_OR_EQUAL and f['value'] == 65 for f in parsed)


def test_should_parse_valid_integer_filter_with_less_than_operator():
    parsed = passive_filter_set.parse(f'age={LESS_THAN}:65')
    assert any(f['field'] == 'age' and f['operator'] == LESS_THAN and f['value'] == 65 for f in parsed)


def test_should_parse_valid_integer_filter_with_less_than_or_equal_operator():
    parsed = passive_filter_set.parse(f'age={LESS_THAN_OR_EQUAL}:65')
    assert any(f['field'] == 'age' and f['operator'] == LESS_THAN_OR_EQUAL and f['value'] == 65 for f in parsed)


def test_should_parse_multiple_comparison_operators_for_single_integer_filter():
    parsed = passive_filter_set.parse(f'age={GREATER_THAN_OR_EQUAL}:60&age={LESS_THAN_OR_EQUAL}:69')
    assert any(f['field'] == 'age' and f['operator'] == GREATER_THAN_OR_EQUAL and f['value'] == 60 for f in parsed)
    assert any(f['field'] == 'age' and f['operator'] == LESS_THAN_OR_EQUAL and f['value'] == 69 for f in parsed)


def test_should_ignore_if_integer_filter_passive_mode_and_value_is_omitted():
    parsed1 = passive_filter_set.parse(f'age=')
    parsed2 = passive_filter_set.parse(f'age')
    parsed3 = passive_filter_set.parse(f'age=gt:')
    parsed4 = passive_filter_set.parse(f'age=gt')
    assert not parsed1
    assert not parsed2
    assert not parsed3
    assert not parsed4


def test_should_raise_error_if_integer_filter_strict_mode_and_value_is_omitted():
    with pytest.raises(InvalidIntegerException):
        strict_filter_set.parse('age=')

    with pytest.raises(InvalidIntegerException):
        strict_filter_set.parse('age')

    with pytest.raises(InvalidIntegerException):
        strict_filter_set.parse(f'age=gt:')
    
    with pytest.raises(InvalidIntegerException):
        strict_filter_set.parse(f'age=gte')


def test_should_raise_error_if_integer_filter_strict_mode_and_invalid_value_passed():
    with pytest.raises(InvalidIntegerException):
        strict_filter_set.parse('age=notaninteger')


# float filter tests
def test_should_parse_valid_float_filter():
    parsed = passive_filter_set.parse('weight=200.621')
    assert any(f['field'] == 'weight' and f['operator'] == EQUAL and f['value'] == 200.621
               for f in parsed)


def test_should_parse_valid_float_filter_with_equal_operator():
    parsed = passive_filter_set.parse(f'weight={EQUAL}:200.621')
    assert any(f['field'] == 'weight' and f['operator'] == EQUAL and f['value'] == 200.621
               for f in parsed)


def test_should_parse_valid_float_filter_with_not_equal_operator():
    parsed = passive_filter_set.parse(f'weight={NOT_EQUAL}:200.621')
    assert any(f['field'] == 'weight' and f['operator'] == NOT_EQUAL and f['value'] == 200.621
               for f in parsed)


def test_should_parse_valid_float_filter_with_greater_than_operator():
    parsed = passive_filter_set.parse(f'weight={GREATER_THAN}:200.621')
    assert any(f['field'] == 'weight' and f['operator'] == GREATER_THAN and f['value'] == 200.621
               for f in parsed)


def test_should_parse_valid_float_filter_with_greater_than_or_equal_operator():
    parsed = passive_filter_set.parse(f'weight={GREATER_THAN_OR_EQUAL}:200.621')
    assert any(f['field'] == 'weight' and f['operator'] == GREATER_THAN_OR_EQUAL and f['value'] == 200.621
               for f in parsed)


def test_should_parse_valid_float_filter_with_less_than_operator():
    parsed = passive_filter_set.parse(f'weight={LESS_THAN}:200.621')
    assert any(f['field'] == 'weight' and f['operator'] == LESS_THAN and f['value'] == 200.621
               for f in parsed)


def test_should_parse_valid_float_filter_with_less_than_or_equal_operator():
    parsed = passive_filter_set.parse(f'weight={LESS_THAN_OR_EQUAL}:200.621')
    assert any(f['field'] == 'weight' and f['operator'] == LESS_THAN_OR_EQUAL and f['value'] == 200.621
               for f in parsed)


def test_should_ignore_if_float_filter_passive_mode_and_value_is_omitted():
    parsed1 = passive_filter_set.parse(f'weight=')
    parsed2 = passive_filter_set.parse(f'weight')
    parsed3 = passive_filter_set.parse(f'weight=gt:')
    parsed4 = passive_filter_set.parse(f'weight=gt')
    assert not parsed1
    assert not parsed2
    assert not parsed3
    assert not parsed4


def test_should_raise_error_if_integer_filter_strict_mode_and_value_is_omitted():
    with pytest.raises(InvalidFloatException):
        strict_filter_set.parse('weight=')

    with pytest.raises(InvalidFloatException):
        strict_filter_set.parse('weight')

    with pytest.raises(InvalidFloatException):
        strict_filter_set.parse(f'weight=gt:')
    
    with pytest.raises(InvalidFloatException):
        strict_filter_set.parse(f'weight=gte')


def test_should_raise_error_if_float_filter_strict_mode_and_invalid_value_passed():
    with pytest.raises(InvalidFloatException):
        strict_filter_set.parse('weight=notafloat')


# boolean filter tests
def test_should_parse_valid_boolean_filter():
    parsed = passive_filter_set.parse('divorced=true')
    assert any(f['field'] == 'divorced' and f['operator'] == EQUAL and f['value'] is True
               for f in parsed)


def test_should_parse_valid_boolean_filter_with_equal_operator():
    parsed = passive_filter_set.parse(f'divorced={EQUAL}:true')
    assert any(f['field'] == 'divorced' and f['operator'] == EQUAL and f['value'] is True
               for f in parsed)


def test_should_parse_valid_boolean_filter_with_not_equal_operator():
    parsed = passive_filter_set.parse(f'divorced={NOT_EQUAL}:true')
    assert any(f['field'] == 'divorced' and f['operator'] == NOT_EQUAL and f['value'] is True
               for f in parsed)


def test_should_raise_error_if_boolean_filter_strict_mode_and_value_is_omitted():
    with pytest.raises(InvalidBooleanException):
        strict_filter_set.parse('divorced=')

    with pytest.raises(InvalidBooleanException):
        strict_filter_set.parse('divorced')

    with pytest.raises(InvalidBooleanException):
        strict_filter_set.parse(f'divorced={NOT_EQUAL}:')
    
    with pytest.raises(InvalidBooleanException):
        strict_filter_set.parse(f'divorced={NOT_EQUAL}')


def test_should_parse_valid_filters():
    parsed = passive_filter_set.parse('name=Ron Swanson&age=65&weight=200.621&divorced=1')
    assert any(f['field'] == 'name' and f['operator'] == EQUAL and f['value'] == 'Ron Swanson'
               for f in parsed)
    assert any(f['field'] == 'age' and f['operator'] == EQUAL and f['value'] == 65 for f in parsed)
    assert any(f['field'] == 'weight' and f['operator'] == EQUAL and f['value'] == 200.621
               for f in parsed)
    assert any(f['field'] == 'divorced' and f['operator'] == EQUAL and f['value'] is True
               for f in parsed)
