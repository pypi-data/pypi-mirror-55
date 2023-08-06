from kakeibox_core.responses.errors.command_error_handler import \
    CommandErrorHandler
import logging


class CommandErrorHandlerLogging(CommandErrorHandler):

    def __init__(self, request):
        self.request = request

    def execute(self):
        logging.exception("An error occurred")
