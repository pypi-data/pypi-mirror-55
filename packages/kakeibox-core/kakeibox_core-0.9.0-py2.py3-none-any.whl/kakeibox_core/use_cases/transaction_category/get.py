from kakeibox_core.use_cases.strategy import UseCaseStrategy
from kakeibox_core.storage_data_bridge.transaction_category import \
    TransactionCategoryBridge
from kakeibox_core.responses.errors.error_handler import ErrorHandler
from kakeibox_core.responses.success.success_handler import SuccessHandler


class TransactionCategoryByCode(UseCaseStrategy):

    def __init__(self, storage_bridge):
        self.storage_data_bridge = TransactionCategoryBridge(storage_bridge)

    def execute(self, transaction_category_code):
        try:
            value = self.storage_data_bridge.get_by_code(
                transaction_category_code)
            return SuccessHandler(value)
        except Exception as error:
            error_response = ErrorHandler(error).handle()
            return error_response
