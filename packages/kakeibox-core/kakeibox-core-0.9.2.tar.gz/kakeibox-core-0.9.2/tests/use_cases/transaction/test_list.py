from kakeibox_core.use_cases.transaction.list import ListTransactions
from kakeibox_storage_memory.storage import StorageTransaction
from kakeibox_storage_memory.bridge import Bridge
import datetime


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_transaction_list(transaction_data):
    before_execute_test()
    end_time = datetime.datetime.now()
    start_time = (end_time - datetime.timedelta(days=10)).timestamp()
    end_time = end_time.timestamp()

    storage = StorageTransaction()
    storage.table = transaction_data
    expenses = [item for item in storage.table.values() if int(start_time) <=
                int(item['timestamp']) <= int(end_time)
                ]
    storage_bridge = Bridge()
    use_case = ListTransactions(storage_bridge)
    result = use_case.execute(start_time, end_time)
    assert result
    assert isinstance(result.value, list)
    assert expenses == result.value
    for element in result.value:
        assert isinstance(element, dict)
