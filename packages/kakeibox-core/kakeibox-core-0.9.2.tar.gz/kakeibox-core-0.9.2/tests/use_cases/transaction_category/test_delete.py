from kakeibox_core.use_cases.transaction_category.delete import \
    DeleteTransactionCategory
from kakeibox_storage_memory.storage import StorageTransactionCategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_use_case_transaction_category_delete(transaction_category_data):
    before_execute_test()
    item = list(transaction_category_data.values())[0]
    storage = StorageTransactionCategory()
    storage.table[item['code']] = item
    assert 1 == len(storage.table)

    storage_bridge = Bridge()
    use_case = DeleteTransactionCategory(storage_bridge)
    result = use_case.execute(item['code'])
    assert isinstance(result.value, bool)
    assert result.value

    storage = StorageTransactionCategory()
    assert 0 == len(storage.table)
