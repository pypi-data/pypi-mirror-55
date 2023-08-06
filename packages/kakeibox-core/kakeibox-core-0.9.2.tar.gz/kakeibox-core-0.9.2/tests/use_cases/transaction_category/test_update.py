from kakeibox_core.use_cases.transaction_category.update import \
    UpdateTransactionCategory
from kakeibox_storage_memory.storage import StorageTransactionCategory
from kakeibox_storage_memory.bridge import Bridge
from time import time


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_use_case_transaction_category_update(transaction_category_data):
    before_execute_test()
    item = list(transaction_category_data.values())[0]
    storage = StorageTransactionCategory()
    storage.table[item['code']] = item
    assert 1 == len(storage.table)

    item['name'] = "new name {}".format(time())

    storage_bridge = Bridge()
    use_case = UpdateTransactionCategory(storage_bridge)
    result = use_case.execute(item['code'], item)
    expected = storage.table[item['code']]

    assert result
    assert isinstance(result.value, dict)
    assert expected['code'] == result.value['code']
    assert expected['name'] == result.value['name']
