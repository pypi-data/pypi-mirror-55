from kakeibox_core.use_cases.strategy import UseCaseStrategy
from kakeibox_core.storage_data_bridge.transaction_subcategory import \
    TransactionSubcategoryBridge
from kakeibox_core.responses.errors.error_handler import ErrorHandler
from kakeibox_core.responses.success.success_handler import SuccessHandler


class ListAllTransactionSubcategories(UseCaseStrategy):

    def __init__(self, storage_bridge):
        self.persistent_data_bridge = TransactionSubcategoryBridge(
            storage_bridge)

    def execute(self):
        try:
            value = self.persistent_data_bridge.list()
            return SuccessHandler(value)
        except Exception as error:
            error_response = ErrorHandler(error).handle()
            return error_response
