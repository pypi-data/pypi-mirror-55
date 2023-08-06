from kakeibox_core.use_cases.income.delete import DeleteIncome
from kakeibox_storage_memory.storage import StorageTransaction
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_income_delete(an_income_data):
    before_execute_test()
    item = an_income_data
    storage = StorageTransaction()
    storage.table[item['uuid']] = item
    assert 1 == len(storage.table)

    storage_bridge = Bridge()
    use_case = DeleteIncome(storage_bridge)
    result = use_case.execute(item['uuid'])
    assert result
    assert isinstance(result.value, bool)
    assert result.value
    assert 0 == len(storage.table)
