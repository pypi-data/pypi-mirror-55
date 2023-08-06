from kakeibox_core.use_cases.expense.update import UpdateExpense
from kakeibox_storage_memory.bridge import Bridge
from kakeibox_storage_memory.storage import StorageTransaction
from faker import Faker
import datetime


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_expense_update(an_expense_data):
    before_execute_test()
    fake = Faker()
    storage = StorageTransaction()
    storage.table[an_expense_data['uuid']] = an_expense_data
    assert 1 == len(storage.table)

    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=10)

    an_expense_data['description'] = fake.sentence()
    an_expense_data['amount'] = fake.pydecimal(
        positive=True, min_value=0, max_value=10000)
    an_expense_data['timestamp'] = fake.unix_time(
        start_datetime=start, end_datetime=end)
    an_expense_data['reference_number'] = fake.bban()

    storage_bridge = Bridge()
    use_case = UpdateExpense(storage_bridge)
    result = use_case.execute(an_expense_data['uuid'], an_expense_data)
    expected = storage.table[an_expense_data['uuid']]

    assert result
    assert isinstance(result.value, dict)
    assert expected['uuid'] == result.value['uuid']
    assert expected['description'] == result.value['description']
    assert expected['amount'] == result.value['amount']
    assert expected['timestamp'] == result.value['timestamp']
    assert expected['reference_number'] == result.value['reference_number']
    assert expected['record_hash'] == result.value['record_hash']
    assert expected['transaction_type_code'] == result.value[
        'transaction_type_code']
    assert expected['transaction_subcategory_code'] == result.value[
        'transaction_subcategory_code']
