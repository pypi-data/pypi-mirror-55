from kakeibox_core.use_cases.transaction_subcategory.update import \
    UpdateTransactionSubcategory
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from kakeibox_storage_memory.bridge import Bridge
from time import time


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_use_case_transaction_subcategory_update(transaction_subcategory_data):
    before_execute_test()
    item = list(transaction_subcategory_data.values())[0]
    storage = StorageTransactionSubcategory()
    storage.table[item['code']] = item
    assert 1 == len(storage.table)

    storage_bridge = Bridge()
    item['name'] = "new name {}".format(time())
    use_case = UpdateTransactionSubcategory(storage_bridge)
    result = use_case.execute(item['code'], item)
    expected = storage.table[item['code']]

    assert result
    assert isinstance(result.value, dict)
    assert expected['code'] == result.value['code']
    assert expected['name'] == result.value['name']
