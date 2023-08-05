from .exception import BasicException


class PreconditionFailedException(BasicException):

    def __init__(self, message, error_code=None):
        BasicException.__init__(self)
        self.status_code = 412
        self.error_code = error_code
        self.message = message
