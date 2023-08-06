from kakeibox_controllers.controllers.expense.get \
    import TransactionExpenseGet
from kakeibox_storage_memory.storage import StorageTransaction
from tests.utils.json import assert_json_dict


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_get_income(expense_dict):
    before_execute_test()
    uuid = expense_dict['uuid']
    storage = StorageTransaction()
    storage.table = {uuid: expense_dict}
    action = TransactionExpenseGet()
    response = action.execute(uuid)
    assert_json_dict(expense_dict, response)
