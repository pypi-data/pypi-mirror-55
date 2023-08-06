from kakeibox_core.use_cases.income.update import UpdateIncome
from kakeibox_storage_memory.storage import StorageTransaction
from kakeibox_storage_memory.bridge import Bridge
from faker import Faker
import datetime


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_use_case_income_update(an_income_data):
    before_execute_test()
    fake = Faker()
    item = an_income_data
    storage = StorageTransaction()
    storage.table[item['uuid']] = item
    assert 1 == len(storage.table)

    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=10)

    item['description'] = fake.sentence()
    item['amount'] = fake.pydecimal(
        positive=True, min_value=0, max_value=10000)
    item['timestamp'] = fake.unix_time(start_datetime=start, end_datetime=end)
    item['reference_number'] = fake.bban()

    storage_bridge = Bridge()
    use_case = UpdateIncome(storage_bridge)
    result = use_case.execute(item['uuid'], item)
    expected = storage.table[item['uuid']]

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
