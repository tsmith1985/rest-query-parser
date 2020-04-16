import pytest

from exceptions import (NullNotAllowedException, InvalidBooleanException, InvalidIntegerException,
                        InvalidFloatException)
from filters import BooleanFilter, FloatFilter, IntegerFilter, StringFilter, DelimitedSetFilter
from operators import (EQUAL, NOT_EQUAL, IN, NOT_IN, GREATER_THAN, GREATER_THAN_OR_EQUAL,
                       LESS_THAN, LESS_THAN_OR_EQUAL)


# string filter tests
def test_should_parse_valid_string():
    f = StringFilter()
    parsed = f.parse('Ron Swanson')
    assert parsed == 'Ron Swanson'


def test_string_filter_should_parse_and_allow_null_by_default():
    f = StringFilter()
    assert f.parse('null') is None
    assert f.parse('NULL') is None
    assert f.parse('none') is None
    assert f.parse('None') is None


def test_string_filter_should_raise_error_if_allow_null_is_false():
    f = StringFilter(allow_null=False)
    with pytest.raises(NullNotAllowedException):
        f.parse('NULL')


def test_string_filter_should_support_these_operators():
    f = StringFilter()
    assert EQUAL in f.operators
    assert NOT_EQUAL in f.operators
    assert IN in f.operators
    assert NOT_IN in f.operators


# integer filter tests
def test_should_parse_valid_integer():
    f = IntegerFilter()
    parsed = f.parse('1')
    assert parsed == 1


def test_integer_filter_should_parse_and_allow_null_by_default():
    f = IntegerFilter()
    assert f.parse('null') is None
    assert f.parse('NULL') is None
    assert f.parse('none') is None
    assert f.parse('None') is None


def test_integer_filter_should_raise_error_if_allow_null_is_false():
    f = IntegerFilter(allow_null=False)
    with pytest.raises(NullNotAllowedException):
        f.parse('none')


def test_integer_filter_should_support_these_operators():
    f = IntegerFilter()
    assert EQUAL in f.operators
    assert NOT_EQUAL in f.operators
    assert GREATER_THAN in f.operators
    assert GREATER_THAN_OR_EQUAL in f.operators
    assert LESS_THAN in f.operators
    assert LESS_THAN_OR_EQUAL in f.operators


def test_integer_filter_should_raise_error_if_input_not_expected_integer_value():
    f = IntegerFilter()
    with pytest.raises(InvalidIntegerException):
        f.parse('notanint')


# float filter tests
def test_should_parse_valid_float():
    f = FloatFilter()
    parsed = f.parse('1.1')
    assert parsed == 1.1


def test_float_filter_should_parse_and_allow_null_by_default():
    f = FloatFilter()
    assert f.parse('null') is None
    assert f.parse('NULL') is None
    assert f.parse('none') is None
    assert f.parse('None') is None


def test_float_filter_should_raise_error_if_allow_null_is_false():
    f = FloatFilter(allow_null=False)
    with pytest.raises(NullNotAllowedException):
        f.parse('null')


def test_float_filter_should_raise_error_if_input_not_expected_float_value():
    f = FloatFilter()
    with pytest.raises(InvalidFloatException):
        f.parse('notafloat')


def test_float_filter_should_support_these_operators():
    f = FloatFilter()
    assert EQUAL in f.operators
    assert NOT_EQUAL in f.operators
    assert GREATER_THAN in f.operators
    assert GREATER_THAN_OR_EQUAL in f.operators
    assert LESS_THAN in f.operators
    assert LESS_THAN_OR_EQUAL in f.operators


# boolean filter tests
def test_should_parse_valid_boolean():
    f = BooleanFilter()
    parsed = f.parse('true')
    assert parsed is True


def test_boolean_filter_should_parse_and_allow_null_by_default():
    f = BooleanFilter()
    assert f.parse('null') is None
    assert f.parse('NULL') is None
    assert f.parse('none') is None
    assert f.parse('None') is None


def test_boolean_filter_should_raise_error_if_allow_null_is_false():
    f = BooleanFilter(allow_null=False)
    with pytest.raises(NullNotAllowedException):
        f.parse('None')


def test_boolean_filter_should_raise_error_if_input_not_expected_boolean_value():
    f = BooleanFilter()
    with pytest.raises(InvalidBooleanException):
        f.parse('notaboolean')


def test_boolean_filter_should_support_these_operators():
    f = BooleanFilter()
    assert EQUAL in f.operators
    assert NOT_EQUAL in f.operators


# delimited set filter tests
def test_should_parse_valid_set():
    f = DelimitedSetFilter(filter_type=IntegerFilter)
    parsed = f.parse('1,2,3')
    assert parsed == [1, 2, 3]
