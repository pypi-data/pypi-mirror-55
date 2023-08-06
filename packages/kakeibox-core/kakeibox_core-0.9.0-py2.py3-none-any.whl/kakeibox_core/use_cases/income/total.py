from kakeibox_core.use_cases.strategy import UseCaseStrategy
from kakeibox_core.storage_data_bridge.transaction import TransactionBridge
from kakeibox_core.responses.errors.error_handler import ErrorHandler
from kakeibox_core.responses.success.success_handler import SuccessHandler


class GetTotalIncome(UseCaseStrategy):

    def __init__(self, storage_bridge):
        self.storage_data_bridge = TransactionBridge(storage_bridge)

    def _list_per_type(self, start, end):
        return self.storage_data_bridge.list_per_type(start, end, 'INC')

    def _sum_all_incomes(self, items):
        total = 0
        for item in items:
            total += item['amount']
        return round(total, 2)

    def execute(self, start_time, end_time):
        try:
            incomes = self._list_per_type(start_time, end_time)
            value = self._sum_all_incomes(incomes)
            return SuccessHandler(value)
        except Exception as error:
            error_response = ErrorHandler(error).handle()
            return error_response
