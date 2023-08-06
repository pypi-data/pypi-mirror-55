from kakeibox_core.use_cases.transaction_subcategory.new import \
    NewTransactionSubcategory
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_use_case_transaction_subcategory_new(transaction_subcategory_data):
    before_execute_test()
    transaction_category = list(transaction_subcategory_data.values())[0]
    storage = StorageTransactionSubcategory()
    assert 0 == len(storage.table)

    storage_bridge = Bridge()
    use_case = NewTransactionSubcategory(storage_bridge)
    result = use_case.execute(transaction_category)
    assert result
    assert isinstance(result.value, dict)

    storage = StorageTransactionSubcategory()
    assert 1 == len(storage.table)
    expected = storage.table[transaction_category['code']]
    assert expected['code'] == result.value['code']
    assert expected['name'] == result.value['name']
