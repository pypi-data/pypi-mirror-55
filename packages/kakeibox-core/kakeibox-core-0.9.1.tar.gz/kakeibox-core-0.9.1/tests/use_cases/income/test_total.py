from kakeibox_core.use_cases.income.total import GetTotalIncome
from kakeibox_storage_memory.storage import StorageTransaction
from kakeibox_storage_memory.bridge import Bridge
import datetime


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_income_total(transaction_total_data):
    before_execute_test()
    end_time = datetime.datetime.now()
    start_time = (end_time - datetime.timedelta(days=10)).timestamp()
    end_time = end_time.timestamp()

    storage = StorageTransaction()
    storage.table = transaction_total_data
    incomes = [item for item in storage.table.values()
               if
               int(start_time) <= int(item['timestamp']) <= int(end_time) and
               item['transaction_type_code'] == 'INC'
               ]
    total_income = 0
    for income in incomes:
        total_income += income['amount']
    total_income = round(total_income, 2)

    storage_brdige = Bridge()
    use_case = GetTotalIncome(storage_brdige)
    result = use_case.execute(start_time, end_time)
    assert result
    assert isinstance(result.value, float)
    assert total_income == result.value
