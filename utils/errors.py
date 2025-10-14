
class ResponseFormatError(Exception):
    """Exception raised when the response format is not as expected"""
    pass

class ResponseNotValidError(Exception):
    """Exception raised when the response is not valid"""
    pass

class ResponseRepeatError(Exception):
    """Exception raised when the response is repeated"""
    pass