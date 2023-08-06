from kakeibox_core.responses.error_response import ErrorResponse
from kakeibox_core.responses.errors.command_error_handler import \
    CommandErrorHandler


class CommandErrorHandlerCreateResponse(CommandErrorHandler):

    def __init__(self, request):
        self.request = request

    def execute(self):
        return ErrorResponse.create_system_error(
            "{} {}".format(self.request.__class__.__name__, self.request))
