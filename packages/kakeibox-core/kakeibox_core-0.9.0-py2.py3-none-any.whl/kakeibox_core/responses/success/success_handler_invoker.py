from kakeibox_core.responses.success.command_success_handler \
    import CommandSuccessHandler


class SuccessfulHandlerInvoker(object):

    _on_logging = None
    _on_create_response = None

    def set_on_logging(self, command):
        self._on_logging = command

    def set_on_create_response(self, command):
        self._on_create_response = command

    def execute(self):
        if isinstance(self._on_logging, CommandSuccessHandler):
            self._on_logging.execute()

        if isinstance(self._on_create_response, CommandSuccessHandler):
            response = self._on_create_response.execute()

        return response
