class DataAccessException(Exception):
    pass

class IncorrectResultSizeDataAccessException(DataAccessException):
    pass

class ArgumentMustBeNamed(DataAccessException):
    def __init__(self, arg_name, msg = ""):
        DataAccessException.__init__(self, msg)
        self.arg_name = arg_name

class InvalidArgumentType(DataAccessException):
    def __init__(self, arg_type, valid_types, msg = ""):
        DataAccessException.__init__(self, msg)
        self.arg_type = arg_type
        self.valid_types = valid_types