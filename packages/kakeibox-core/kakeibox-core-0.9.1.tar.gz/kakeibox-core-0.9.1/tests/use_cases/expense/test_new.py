from kakeibox_core.use_cases.expense.new import NewExpense
from kakeibox_storage_memory.bridge import Bridge
from kakeibox_storage_memory.storage import StorageTransaction


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_expense_new(an_expense_data):
    before_execute_test()
    transaction_dict = an_expense_data
    storage = StorageTransaction()
    assert 0 == len(storage.table)

    storage_bridge = Bridge()
    use_case = NewExpense(storage_bridge)
    result = use_case.execute(transaction_dict)
    assert result
    assert isinstance(result.value, dict)

    storage = StorageTransaction()
    assert 1 == len(storage.table)

    new_one = storage.table[transaction_dict['uuid']]
    assert result.value['uuid'] == new_one['uuid']
    assert result.value['description'] == new_one['description']
    assert result.value['amount'] == new_one['amount']
    assert result.value['timestamp'] == new_one['timestamp']
    assert result.value['record_hash'] == new_one['record_hash']
    assert result.value['reference_number'] == new_one['reference_number']
    assert result.value['transaction_type_code'] == new_one[
        'transaction_type_code']
    assert result.value['transaction_subcategory_code'] == new_one[
        'transaction_subcategory_code']
