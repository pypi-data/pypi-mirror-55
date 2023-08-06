from kakeibox_controllers.controllers.expense.delete \
    import ExpenseDelete
from kakeibox_storage_memory.storage import StorageTransaction


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_delete_transaction_category(income_dict):
    before_execute_test()
    code = income_dict['uuid']
    storage = StorageTransaction()
    storage.table = {code: income_dict}
    assert len(storage.table) == 1
    action = ExpenseDelete()
    response = action.execute(code)
    assert "true" == response
    assert len(storage.table) == 0
