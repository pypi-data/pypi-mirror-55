from kakeibox_core.use_cases.strategy import UseCaseStrategy
from kakeibox_core.storage_data_bridge.transaction import TransactionBridge
from kakeibox_core.responses.errors.error_handler import ErrorHandler
from kakeibox_core.responses.success.success_handler import SuccessHandler


class ListTransactions(UseCaseStrategy):

    def __init__(self, storage_bridge):
        self.storage_data_bridge = TransactionBridge(storage_bridge)

    def execute(self, start_time, end_time):
        try:
            value = self.storage_data_bridge.list(start_time, end_time)
            return SuccessHandler(value)
        except Exception as error:
            error_response = ErrorHandler(error).handle()
            return error_response
