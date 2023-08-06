import pytest
import datetime
from faker import Faker
from tests.fixtures.kakeibox_core_transaction_data import TRANSACTION_DATA


@pytest.fixture()
def transaction_category_data():
    return {
        'SUR':
            {
                'code': 'SUR',
                'name': 'Survival'
            },
        'OPT':
            {
                'code': 'OPT',
                'name': 'Optional'
            },
        'CUL':
            {
                'code': 'CUL',
                'name': 'Culture'
            },
        'EXT':
            {
                'code': 'EXT',
                'name': 'Extra'
            }
    }


@pytest.fixture()
def transaction_subcategory_data():
    return {
        "FOD": {
            "code": "FOD",
            "name": "Food",
            "transaction_category_code": 'SUR',
        },
        "REN": {
            "code": "REN",
            "name": "Rent",
            "transaction_category_code": 'SUR',
        },
        "TRA": {
            "code": "TRA",
            "name": "Transport",
            "transaction_category_code": 'SUR',
        },
        "KID": {
            "code": "KID",
            "name": "Kids",
            "transaction_category_code": 'SUR',
        },
        "RES": {
            "code": "RES",
            "name": "Restaurant",
            "transaction_category_code": 'OPT',
        },
        "SHO": {
            "code": "SHO",
            "name": "Shopping",
            "transaction_category_code": 'OPT',
        },
        "BOK": {
            "code": "BOK",
            "name": "Books",
            "transaction_category_code": 'CUL',
        },
        "MUS": {
            "code": "MUS",
            "name": "Music",
            "transaction_category_code": 'CUL',
        },
        "SHW": {
            "code": "SHW",
            "name": "Shows",
            "transaction_category_code": 'CUL',
        },
        "MOV": {
            "code": "MOV",
            "name": "Movies",
            "transaction_category_code": 'CUL',
        },
        "MAG": {
            "code": "MAG",
            "name": "Magazines",
            "transaction_category_code": 'CUL',
        },
        "GIF": {
            "code": "GIF",
            "name": " Gifts",
            "transaction_category_code": 'EXT',
        },
        "REP": {
            "code": "REP",
            "name": "Repairs",
            "transaction_category_code": 'EXT',
        },
        "FUR": {
            "code": "FUR",
            "name": "Furniture",
            "transaction_category_code": 'EXT',
        }
    }


def _create_fake_transaction(transaction_type_code=None, amount=None):
    fake = Faker()
    if not transaction_type_code:
        transaction_type_code='EXP'
    end_datetime = datetime.datetime.now()
    start_datetime = end_datetime - datetime.timedelta(days=10)
    if not amount:
        amount = fake.pydecimal(positive=True, min_value=0, max_value=100000)

    return dict(
        transaction_type_code=transaction_type_code,
        transaction_subcategory_code='FOD',
        uuid=fake.uuid4(),
        description=fake.sentence(),
        amount=amount,
        timestamp=fake.unix_time(start_datetime=start_datetime,
                                 end_datetime=end_datetime),
        reference_number=fake.bban(),
        record_hash=''
    )


def _create_fake_expense(amount=None):
    return _create_fake_transaction(amount=amount)


def _create_fake_income(amount=None):
    transaction_type_code = 'INC'
    return _create_fake_transaction(
        transaction_type_code=transaction_type_code, amount=amount)


@pytest.fixture()
def transaction_data():
    return TRANSACTION_DATA


@pytest.fixture()
def an_expense_data():
    return _create_fake_expense()


@pytest.fixture()
def an_income_data():
    return _create_fake_income()


@pytest.fixture()
def transaction_total_data():
    transactions = {}
    for _ in range(1, 11):
        item = _create_fake_income(1000.10)
        transactions.setdefault(item['uuid'], item)

    for _ in range(1, 11):
        item = _create_fake_expense(100.20)
        transactions.setdefault(item['uuid'], item)
    return transactions
