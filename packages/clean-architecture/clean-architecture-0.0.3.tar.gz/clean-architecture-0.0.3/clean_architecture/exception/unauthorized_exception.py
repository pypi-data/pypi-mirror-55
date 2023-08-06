from .exception import BasicException


class UnauthorizedException(BasicException):

    def __init__(self, message, error_code=None):
        BasicException.__init__(self)
        self.status_code = 401
        self.error_code = error_code
        self.message = message
