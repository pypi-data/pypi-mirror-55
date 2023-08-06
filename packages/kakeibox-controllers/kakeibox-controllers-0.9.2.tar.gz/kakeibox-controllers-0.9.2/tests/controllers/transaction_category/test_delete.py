from kakeibox_controllers.controllers.transaction_category.delete \
    import TransactionCategoryDelete
from kakeibox_storage_memory.storage import StorageTransactionCategory


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_delete_transaction_category(transaction_category_dict):
    before_execute_test()
    code = transaction_category_dict['code']
    storage = StorageTransactionCategory()
    storage.table = {code: transaction_category_dict}
    assert len(storage.table) == 1
    action = TransactionCategoryDelete()
    response = action.execute(code)
    assert "true" == response
    assert len(storage.table) == 0
