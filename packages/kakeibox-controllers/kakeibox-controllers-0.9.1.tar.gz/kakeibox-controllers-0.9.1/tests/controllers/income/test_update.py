from kakeibox_controllers.controllers.income.update \
    import IncomeUpdate
from kakeibox_storage_memory.storage import StorageTransaction
from tests.utils.json import assert_json
import json


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_update_income(income_dict):
    before_execute_test()
    uuid = income_dict['uuid']
    storage = StorageTransaction()
    storage.table = {uuid: income_dict}

    json_update_income_dict = {"uuid": uuid, "transaction": json.dumps(income_dict)}
    action = IncomeUpdate()
    response = action.execute(**json_update_income_dict)
    assert_json(json_update_income_dict['transaction'], response)

