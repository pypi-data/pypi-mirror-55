class CommandErrorHandler(object):

    def __init__(self, request):
        self.request = request

    def execute(self):
        raise Exception("CommandErrorHandler is not implemented")
