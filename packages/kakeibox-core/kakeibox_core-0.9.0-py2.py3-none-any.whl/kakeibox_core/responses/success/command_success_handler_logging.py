from kakeibox_core.responses.success.command_success_handler \
    import CommandSuccessHandler
import logging


class CommandSuccessHandlerLogging(CommandSuccessHandler):

    def __init__(self, request):
        self.request = request

    def execute(self):
        logging.info(self.request)
