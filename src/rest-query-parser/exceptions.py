class FilterException(Exception):
    """base class for other filter exceptions"""
    pass


class NullNotAllowedException(FilterException):
    """raised when input is a null value but null is not allowed"""
    pass


class InvalidIntegerException(FilterException):
    """raised when input is not an expected integer value"""
    pass


class InvalidFloatException(FilterException):
    """raised when input is not an expected float value"""
    pass


class InvalidBooleanException(FilterException):
    """raised when input is not an expected boolean value"""
    pass


class InvalidWholeNumberException(FilterException):
    """raised when input is not an expected whole number value"""
    pass


class InvalidOperatorException(FilterException):
    """raised when input is not an expected operator"""
    pass
