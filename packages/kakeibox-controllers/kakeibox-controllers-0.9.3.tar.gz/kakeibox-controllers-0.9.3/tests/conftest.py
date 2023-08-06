from tests.fixtures.kakeibox_controllers_transaction_data \
    import TRANSACTION_DATA
import pytest
from faker import Faker
import datetime
import json


@pytest.fixture()
def transaction_data():
    return TRANSACTION_DATA


@pytest.fixture()
def transaction_category_str():
    return """{"code": "SUR", "name": "Survival"}"""


@pytest.fixture()
def transaction_category_dict():
    return {"code": "SUR", "name": "Survival"}


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
    }


@pytest.fixture()
def transaction_subcategory_str():
    return """{"code": "RES", "name": "Restaurant", "transaction_category_code": "OPT"}"""


@pytest.fixture()
def transaction_subcategory_dict():
    return {"code": "RES", "name": "Restaurant", "transaction_category_code": 'OPT'}


@pytest.fixture()
def an_income_data():
    return _create_fake_income()


def _create_fake_income(amount=None):
    transaction_type_code = 'INC'
    return _create_fake_transaction(
        transaction_type_code=transaction_type_code, amount=amount)


def _create_fake_transaction(transaction_type_code=None, amount=None):
    fake = Faker()
    if not transaction_type_code:
        transaction_type_code='EXP'
    end_datetime = datetime.datetime.now()
    start_datetime = end_datetime - datetime.timedelta(days=10)
    if not amount:
        amount = fake.pyfloat(positive=True, min_value=0,
                                    max_value=100000)

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


@pytest.fixture()
def income_dict():
    return _create_fake_transaction(transaction_type_code="INC")


@pytest.fixture()
def income_str():
    income = _create_fake_transaction(transaction_type_code="INC")
    return json.dumps(income)


@pytest.fixture()
def expense_dict():
    return _create_fake_transaction(transaction_type_code="EXP")


@pytest.fixture()
def expense_str():
    income = _create_fake_transaction(transaction_type_code="EXP")
    return json.dumps(income)
