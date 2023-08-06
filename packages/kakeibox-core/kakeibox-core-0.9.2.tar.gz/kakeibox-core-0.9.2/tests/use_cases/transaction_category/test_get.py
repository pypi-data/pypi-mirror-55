from kakeibox_core.use_cases.transaction_category.get import \
    TransactionCategoryByCode
from kakeibox_storage_memory.storage import StorageTransactionCategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_use_case_transaction_category_get(transaction_category_data):
    before_execute_test()
    item = list(transaction_category_data.values())[0]
    storage = StorageTransactionCategory()
    storage.table[item['code']] = item
    assert 1 == len(storage.table)

    storage_bridge = Bridge()
    use_case = TransactionCategoryByCode(storage_bridge)
    result = use_case.execute(item['code'])
    assert isinstance(result.value, dict)
    assert item['code'] == result.value['code']
    assert item['name'] == result.value['name']
