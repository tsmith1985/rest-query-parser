from exceptions import FilterException, InvalidOperatorException
from filters import Filter, WholeNumberFilter
from operators import (ALL, EQUAL, NOT_EQUAL, IN, NOT_IN, GREATER_THAN, GREATER_THAN_OR_EQUAL,
                       LESS_THAN, LESS_THAN_OR_EQUAL)


class FilterSet:
    def __init__(self, strict=False):
        self.strict = strict

    def parse(self, qs):
        parts = qs.split('&')
        filters = [p for p in dir(self) if isinstance(getattr(self, p), Filter)]
        parsed = []

        for part in parts:
            ignore = False

            field, exp = part.split('=') if '=' in part else [part, '']

            if ':' in exp:
                operator, value = exp.split(':')
            elif exp in ALL:
                operator = exp
                value = ''
            else:
                operator = EQUAL
                value = exp

            if field in filters:
                f = getattr(self, field)

                if operator in f.operators:
                    try:
                        value = f.parse(value)
                    except FilterException as ex:
                        if self.strict:
                            raise ex
                        else:
                            ignore = True

                    if not ignore:
                        parsed.append({
                            'field': field,
                            'operator': operator,
                            'value': value
                        })
                elif self.strict:
                    raise InvalidOperatorException()

        return parsed


class PaginationFilterSet(FilterSet):
    limit = WholeNumberFilter(allow_null=False, operators=[EQUAL])
    offset = WholeNumberFilter(allow_null=False, operators=[EQUAL])


#class ProjectionFilterSet(FilterSet):
#    fields = DelimitedSetFilter(StringFilter)
