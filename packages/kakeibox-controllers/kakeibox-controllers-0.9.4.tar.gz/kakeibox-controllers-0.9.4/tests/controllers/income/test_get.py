from kakeibox_controllers.controllers.income.get \
    import TransactionIncomeGet
from kakeibox_storage_memory.storage import StorageTransaction
from tests.utils.json import assert_json_dict


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_get_income(income_dict):
    before_execute_test()
    uuid = income_dict['uuid']
    storage = StorageTransaction()
    storage.table = {uuid: income_dict}
    action = TransactionIncomeGet()
    response = action.execute(uuid)
    assert_json_dict(income_dict, response)
