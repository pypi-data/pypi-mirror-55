from kakeibox_core.use_cases.expense.get import GetExpenseByUUID
from kakeibox_storage_memory.bridge import Bridge
from kakeibox_storage_memory.storage import StorageTransaction


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_expense_get(an_expense_data):
    before_execute_test()
    item = an_expense_data
    storage = StorageTransaction()
    storage.table[item['uuid']] = item
    assert 1 == len(storage.table)

    storage_bridge = Bridge()
    use_case = GetExpenseByUUID(storage_bridge)
    result = use_case.execute(item['uuid'])
    expected = storage.table[item['uuid']]

    assert result
    assert isinstance(result.value, dict)
    assert expected['uuid'] == result.value['uuid']
    assert expected['description'] == result.value['description']
    assert expected['amount'] == result.value['amount']
    assert expected['timestamp'] == result.value['timestamp']
    assert expected['reference_number'] == result.value['reference_number']
    assert expected['record_hash'] == result.value['record_hash']
    assert expected['transaction_type_code'] == result.value[
        'transaction_type_code']
    assert expected['transaction_subcategory_code'] == result.value[
        'transaction_subcategory_code']
