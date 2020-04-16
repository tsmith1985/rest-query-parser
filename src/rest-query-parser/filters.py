from constants import FALSY_VALUES, TRUTHY_VALUES, NULL_VALUES
from exceptions import (NullNotAllowedException, InvalidBooleanException, InvalidIntegerException,
                        InvalidFloatException, InvalidWholeNumberException)
from operators import (EQUAL, NOT_EQUAL, IN, NOT_IN, GREATER_THAN, GREATER_THAN_OR_EQUAL,
                       LESS_THAN, LESS_THAN_OR_EQUAL)
from utils import coalesce


class Filter:
    def __init__(self, operators=None, allow_null=True):
        self.allow_null = allow_null
        self.operators = coalesce(operators, self.operators)

    def parse(self, value):
        parsed = str(value).strip()

        if parsed.lower() in NULL_VALUES:
            if not self.allow_null:
                raise NullNotAllowedException()

            return None

        return parsed


class BooleanFilter(Filter):
    operators = (EQUAL, NOT_EQUAL)

    def parse(self, value):
        parsed = super().parse(value)

        if parsed is None:
            return parsed

        elif parsed.lower() in TRUTHY_VALUES:
            return True
        elif parsed.lower() in FALSY_VALUES:
            return False

        raise InvalidBooleanException()


class NumericFilter(Filter):
    operators = (EQUAL, NOT_EQUAL, GREATER_THAN, GREATER_THAN_OR_EQUAL, LESS_THAN,
                 LESS_THAN_OR_EQUAL)

    def parse(self, value):
        parsed = super().parse(value)
        return parsed


class FloatFilter(NumericFilter):
    def parse(self, value):
        parsed = super().parse(value)

        if parsed is None:
            return parsed

        try:
            parsed = float(parsed)
        except ValueError:
            raise InvalidFloatException()

        return parsed


class IntegerFilter(NumericFilter):
    def parse(self, value):
        parsed = super().parse(value)

        if parsed is None:
            return parsed

        try:
            parsed = int(parsed)
        except ValueError:
            raise InvalidIntegerException()

        return parsed


class StringFilter(Filter):
    operators = (EQUAL, NOT_EQUAL, IN, NOT_IN)


class WholeNumberFilter(NumericFilter):
    def parse(self, value):
        parsed = super().parse(value)

        if parsed is None:
            return parsed

        try:
            parsed = int(parsed)
        except ValueError:
            raise InvalidWholeNumberException()

        if parsed < 0:
            raise InvalidWholeNumberException()

        return parsed


class DelimitedSetFilter(Filter):
    operators = (EQUAL, NOT_EQUAL)

    def __init__(self, *args, **kwargs):
        self.filter_type = kwargs.get('filter_type', StringFilter)

    def parse(self, value):
        parsed = super().parse(value)

        if parsed is None:
            return [parsed]

        parsed = parsed.split(',')
        f = self.filter_type()

        parsed = [f.parse(value) for value in parsed]
        print(parsed)

        return parsed
