from kakeibox_controllers.controllers.transaction_category.list \
    import TransactionCategoryList
from kakeibox_storage_memory.storage import StorageTransactionCategory
from tests.utils.json import assert_json_list

def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_list_transaction_category(transaction_category_data):
    before_execute_test()
    storage = StorageTransactionCategory()
    storage.table = transaction_category_data
    action = TransactionCategoryList()
    response = action.execute()
    assert_json_list(transaction_category_data, response)
