from kakeibox_core.use_cases.strategy import UseCaseStrategy
from kakeibox_core.storage_data_bridge.transaction import TransactionBridge
from kakeibox_core.responses.errors.error_handler import ErrorHandler
from kakeibox_core.responses.success.success_handler import SuccessHandler


class CalculateSaving(UseCaseStrategy):

    def __init__(self, storage_bridge):
        self.storage_data_bridge = TransactionBridge(storage_bridge)

    def _get_total_by_type(self, start_time, end_time, transaction_type):
        total = 0
        items = self.storage_data_bridge.list_per_type(
            start_time, end_time, transaction_type)

        for item in items:
            total += item['amount']
        return round(total, 2)

    def _get_total_income(self, start_time, end_time):
        return self._get_total_by_type(start_time, end_time, 'INC')

    def _get_total_expense(self, start_time, end_time):
        return self._get_total_by_type(start_time, end_time, 'EXP')

    def execute(self, start_time, end_time):
        try:
            incomes = self._get_total_income(start_time, end_time)
            expenses = self._get_total_expense(start_time, end_time)
            saving = incomes - expenses
            return SuccessHandler(saving)
        except Exception as error:
            error_response = ErrorHandler(error).handle()
            return error_response
