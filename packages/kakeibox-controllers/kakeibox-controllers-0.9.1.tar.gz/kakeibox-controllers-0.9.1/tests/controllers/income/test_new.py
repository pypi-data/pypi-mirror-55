from kakeibox_controllers.controllers.income.new \
    import IncomeNew
from kakeibox_storage_memory.storage import StorageTransaction
from tests.utils.json import assert_json


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_new_income(income_str):
    before_execute_test()
    action = IncomeNew()
    response = action.execute(income_str)
    assert_json(income_str, response)
