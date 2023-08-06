from kakeibox_core.responses.errors.error_handler_invoker \
    import ErrorHandlerInvoker
from kakeibox_core.responses.errors.command_error_handler_create_response \
    import CommandErrorHandlerCreateResponse
from kakeibox_core.responses.errors.command_error_handler_logging \
    import CommandErrorHandlerLogging


class ErrorHandler(object):
    def __init__(self, error_exception):
        self.error_exception = error_exception

    def handle(self):
        invoker = ErrorHandlerInvoker()
        invoker.set_on_logging(
            CommandErrorHandlerLogging(self.error_exception))
        invoker.set_on_create_response(
            CommandErrorHandlerCreateResponse(self.error_exception))
        return invoker.execute()
