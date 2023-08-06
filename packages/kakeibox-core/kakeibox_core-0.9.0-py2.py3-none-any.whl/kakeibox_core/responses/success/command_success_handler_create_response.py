from kakeibox_core.responses.successful_response import SuccessfulResponse
from kakeibox_core.responses.success.command_success_handler \
    import CommandSuccessHandler


class CommandSuccessHandlerCreateResponse(CommandSuccessHandler):

    def __init__(self, request):
        self.request = request

    def execute(self):
        return SuccessfulResponse()
