'''
@author: somit
This file contains all the custom exceptions
'''


class DataNotFoundError(Exception):
    pass


class OtpFailedException(Exception):
    def __init__(self, arg):
        self.msg = arg


class ParamToBeFunctionException(Exception):
    def __init__(self, message="Param should be a function not a string or other type"):
        self.msg = message