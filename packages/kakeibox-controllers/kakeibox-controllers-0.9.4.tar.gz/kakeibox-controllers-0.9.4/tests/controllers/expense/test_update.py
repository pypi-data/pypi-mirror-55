from kakeibox_controllers.controllers.expense.update \
    import ExpenseUpdate
from kakeibox_storage_memory.storage import StorageTransaction
from tests.utils.json import assert_json
import json


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_update_expense(expense_dict):
    before_execute_test()
    uuid = expense_dict['uuid']
    storage = StorageTransaction()
    storage.table = {uuid: expense_dict}

    json_update_income_dict = {"uuid": uuid, "transaction": json.dumps(expense_dict)}
    action = ExpenseUpdate()
    response = action.execute(**json_update_income_dict)
    assert_json(json_update_income_dict['transaction'], response)

