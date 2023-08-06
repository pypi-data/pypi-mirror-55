from kakeibox_core.responses.success.success_handler_invoker \
    import SuccessfulHandlerInvoker
from kakeibox_core.responses.errors.command_error_handler_create_response \
    import CommandErrorHandlerCreateResponse
from kakeibox_core.responses.success.command_success_handler_logging \
    import CommandSuccessHandlerLogging


class SuccessHandler(object):
    def __init__(self, value):
        self.value = value

    def handle(self):
        invoker = SuccessfulHandlerInvoker()
        invoker.set_on_logging(
            CommandSuccessHandlerLogging(self.value))
        invoker.set_on_create_response(
            CommandErrorHandlerCreateResponse(self.value))
        return invoker.execute()
