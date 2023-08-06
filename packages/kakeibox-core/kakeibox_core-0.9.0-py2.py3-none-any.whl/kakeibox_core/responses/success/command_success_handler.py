class CommandSuccessHandler(object):

    def __init__(self, request):
        self.request = request

    def execute(self):
        raise Exception("CommandSuccessHandler is not implemented")
