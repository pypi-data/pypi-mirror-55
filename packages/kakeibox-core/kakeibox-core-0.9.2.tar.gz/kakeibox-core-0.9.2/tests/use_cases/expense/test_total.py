from kakeibox_core.use_cases.expense.total import GetTotalExpense
from kakeibox_storage_memory.bridge import Bridge
from kakeibox_storage_memory.storage import StorageTransaction
import datetime


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_expense_total(transaction_total_data):
    before_execute_test()
    end_time = datetime.datetime.now()
    start_time = (end_time - datetime.timedelta(days=10)).timestamp()
    end_time = end_time.timestamp()

    storage = StorageTransaction()
    storage.table = transaction_total_data
    expenses = [item for item in storage.table.values()
                if int(start_time) <= int(item['timestamp']) <= int(end_time)
                and item['transaction_type_code'] == 'EXP'
                ]
    total_expense = 0
    for expense in expenses:
        total_expense += expense['amount']
    total_expense = round(total_expense, 2)

    storage_bridge = Bridge()
    use_case = GetTotalExpense(storage_bridge)
    result = use_case.execute(start_time, end_time)
    assert result
    assert isinstance(result.value, float)
    assert total_expense == result.value
