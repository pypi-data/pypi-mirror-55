from kakeibox_core.use_cases.expense.delete import DeleteExpense
from kakeibox_storage_memory.bridge import Bridge
from kakeibox_storage_memory.storage import StorageTransaction


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_expense_delete(an_expense_data):
    before_execute_test()
    item = an_expense_data
    storage = StorageTransaction()
    storage.table[item['uuid']] = item
    assert 1 == len(storage.table)

    storage_bridge = Bridge()
    use_case = DeleteExpense(storage_bridge)
    result = use_case.execute(item['uuid'])
    assert result
    assert isinstance(result.value, bool)
    assert result.value
    assert 0 == len(storage.table)
