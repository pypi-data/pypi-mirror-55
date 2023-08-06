from kakeibox_core.use_cases.transaction_subcategory.list_all import \
    ListAllTransactionSubcategories
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_use_case_transaction_subcategory_list(transaction_subcategory_data):
    before_execute_test()
    storage = StorageTransactionSubcategory()
    storage.table = transaction_subcategory_data
    transaction_categories = list(storage.table.values())

    storage_bridge = Bridge()
    use_case = ListAllTransactionSubcategories(storage_bridge)
    result = use_case.execute()
    assert result
    assert isinstance(result.value, list)
    assert transaction_categories == result.value
    for element in result.value:
        assert isinstance(element, dict)
