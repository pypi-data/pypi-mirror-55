from kakeibox_core.responses.errors.command_error_handler import \
    CommandErrorHandler


class ErrorHandlerInvoker(object):

    _on_logging = None
    _on_create_response = None

    def set_on_logging(self, command):
        self._on_logging = command

    def set_on_create_response(self, command):
        self._on_create_response = command

    def execute(self):
        if isinstance(self._on_logging, CommandErrorHandler):
            self._on_logging.execute()

        if isinstance(self._on_create_response, CommandErrorHandler):
            error_response = self._on_create_response.execute()

        return error_response
