from kakeibox_core.use_cases.transaction_subcategory.get import \
    TransactionSubcategoryByCode
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_use_case_transaction_subcategory_get(transaction_subcategory_data):
    before_execute_test()
    item = list(transaction_subcategory_data.values())[0]
    storage = StorageTransactionSubcategory()
    storage.table[item['code']] = item
    assert 1 == len(storage.table)

    storage_bridge = Bridge()
    use_case = TransactionSubcategoryByCode(storage_bridge)
    result = use_case.execute(item['code'])
    assert result
    assert isinstance(result.value, dict)
    assert item['code'] == result.value['code']
    assert item['name'] == result.value['name']
