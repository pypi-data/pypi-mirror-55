from kakeibox_core.use_cases.transaction_category.new import \
    NewTransactionCategory
from kakeibox_storage_memory.storage import StorageTransactionCategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_use_case_transaction_category_new(transaction_category_data):
    before_execute_test()
    transaction_category = list(transaction_category_data.values())[0]
    storage = StorageTransactionCategory()
    assert 0 == len(storage.table)

    storage_bridge = Bridge()
    use_case = NewTransactionCategory(storage_bridge)
    result = use_case.execute(transaction_category)
    assert result
    assert isinstance(result.value, dict)
    assert 1 == len(storage.table)

    new_one = storage.table[result.value['code']]
    assert result.value['code'] == new_one['code']
    assert result.value['name'] == new_one['name']
