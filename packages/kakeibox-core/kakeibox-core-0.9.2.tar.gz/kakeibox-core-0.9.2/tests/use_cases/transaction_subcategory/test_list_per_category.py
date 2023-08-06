from kakeibox_core.use_cases.transaction_subcategory.list_per_category import \
    ListTransactionSubcategoriesPerCategory
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from kakeibox_storage_memory.bridge import Bridge


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def _get_category_subcategories(storage, category):
    return [item for item in storage.table.values()
            if item['transaction_category_code'] == category
            ]


def _verify_category(storage, category):
    transaction_subcategories = _get_category_subcategories(storage, category)
    first_subcategory = transaction_subcategories[0]
    storage_bridge = Bridge()
    use_case = ListTransactionSubcategoriesPerCategory(storage_bridge)
    result = use_case.execute(category)
    assert result
    assert isinstance(result.value, list)
    assert transaction_subcategories == result.value
    assert first_subcategory['transaction_category_code'] == category
    for element in result.value:
        assert isinstance(element, dict)


def test_use_case_transaction_subcategory_list_per_category(
        transaction_subcategory_data):
    before_execute_test()
    storage = StorageTransactionSubcategory()
    storage.table = transaction_subcategory_data

    for transaction_subcategory in transaction_subcategory_data.values():
        category = transaction_subcategory['transaction_category_code']
        _verify_category(storage, category)
