from kakeibox_core.use_cases.transaction_subcategory.delete import \
    DeleteTransactionSubcategory
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_use_case_transaction_subcategory_delete(transaction_subcategory_data):
    before_execute_test()
    item = list(transaction_subcategory_data.values())[0]
    storage = StorageTransactionSubcategory()
    storage.table[item['code']] = item
    assert 1 == len(storage.table)

    storage_bridge = Bridge()
    use_case = DeleteTransactionSubcategory(storage_bridge)
    result = use_case.execute(item['code'])
    assert isinstance(result.value, bool)
    assert result.value
    assert 0 == len(storage.table)
