from kakeibox_controllers.controllers.transaction_subcategory.list \
    import TransactionSubcategoryList
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from tests.utils.json import assert_json_list


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_list_transaction_category(transaction_subcategory_data):
    before_execute_test()
    storage = StorageTransactionSubcategory()
    storage.table = transaction_subcategory_data
    action = TransactionSubcategoryList()
    response = action.execute()
    assert_json_list(transaction_subcategory_data, response)
