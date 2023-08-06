from kakeibox_controllers.controllers.transaction_category.new \
    import TransactionCategoryNew
from kakeibox_storage_memory.storage import StorageTransactionCategory
from tests.utils.json import assert_json


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_new_transaction_category(transaction_category_str):
    before_execute_test()
    action = TransactionCategoryNew()
    response = action.execute(transaction_category_str)
    assert_json(transaction_category_str, response)
