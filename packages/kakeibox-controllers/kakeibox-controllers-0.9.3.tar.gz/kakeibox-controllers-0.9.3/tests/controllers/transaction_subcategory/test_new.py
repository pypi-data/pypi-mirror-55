from kakeibox_controllers.controllers.transaction_subcategory.new \
    import TransactionSubcategoryNew
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from tests.utils.json import assert_json


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_new_transaction_category(transaction_subcategory_str):
    before_execute_test()
    action = TransactionSubcategoryNew()
    response = action.execute(transaction_subcategory_str)
    assert_json(transaction_subcategory_str, response)
