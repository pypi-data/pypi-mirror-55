class SuccessfulResponse(object):
    SUCCESS = 'Success'

    def __init__(self, value):
        self.type = self.SUCCESS
        self.value = value

    def __bool__(self):
        return True
