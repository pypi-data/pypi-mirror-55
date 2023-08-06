from kakeibox_core.use_cases.transaction_category.list import \
    ListTransactionCategories
from kakeibox_storage_memory.storage import StorageTransactionCategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_use_case_transaction_category_list(transaction_category_data):
    before_execute_test()
    storage = StorageTransactionCategory()
    storage.table = transaction_category_data
    transaction_categories = list(storage.table.values())
    storage_brdige = Bridge()
    use_case = ListTransactionCategories(storage_brdige)
    result = use_case.execute()
    assert transaction_categories == result.value
    assert result
    assert isinstance(result.value, list)
    for element in result.value:
        assert isinstance(element, dict)
