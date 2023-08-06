from kakeibox_controllers.controllers.expense.new \
    import ExpenseNew
from kakeibox_storage_memory.storage import StorageTransaction
from tests.utils.json import assert_json


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_new_expense(expense_str):
    before_execute_test()
    action = ExpenseNew()
    response = action.execute(expense_str)
    assert_json(expense_str, response)
