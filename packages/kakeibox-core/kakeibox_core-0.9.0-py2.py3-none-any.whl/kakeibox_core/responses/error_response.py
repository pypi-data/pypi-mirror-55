class ErrorResponse(object):
    RESOURCE_ERROR = 'ResourceError'
    PARAMETERS_ERROR = 'ParametersError'
    SYSTEM_ERROR = 'SystemError'

    def __init__(self, type_error, message):
        self.type = type_error
        self.message = self._format_message(message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg

    @classmethod
    def create_system_error(cls, message=None):
        return cls(cls.SYSTEM_ERROR, message)

    def __bool__(self):
        return False

    @property
    def value(self):
        return {'type': self.type, 'message': self.message}
