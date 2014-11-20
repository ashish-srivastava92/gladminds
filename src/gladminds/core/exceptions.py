'''
@author: somit
This file contains all the custom exceptions
'''


class DataNotFoundError(Exception):
    pass


class OtpFailedException(Exception):
    def __init__(self, arg):
        # Set some exception infomation
        self.msg = arg