from kakeibox_controllers.controllers.transaction_subcategory.delete \
    import TransactionSubcategoryDelete
from kakeibox_storage_memory.storage import StorageTransactionSubcategory


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_delete_transaction_subcategory(transaction_subcategory_dict):
    before_execute_test()
    code = transaction_subcategory_dict['code']
    storage = StorageTransactionSubcategory ()
    storage.table = {code: transaction_subcategory_dict}
    assert len(storage.table) == 1
    action = TransactionSubcategoryDelete()
    response = action.execute(code)
    assert "true" == response
    assert len(storage.table) == 0
