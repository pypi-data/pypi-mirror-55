from kakeibox_core.use_cases.strategy import UseCaseStrategy
from kakeibox_core.storage_data_bridge.transaction_category import \
    TransactionCategoryBridge
from kakeibox_core.responses.errors.error_handler import ErrorHandler
from kakeibox_core.responses.success.success_handler import SuccessHandler


class NewTransactionCategory(UseCaseStrategy):

    def __init__(self, storage_bridge):
        self.storage_data_bridge = TransactionCategoryBridge(storage_bridge)

    def execute(self, transaction_category):
        try:
            value = self.storage_data_bridge.new(transaction_category)
            return SuccessHandler(value)
        except Exception as error:
            error_response = ErrorHandler(error).handle()
            return error_response
