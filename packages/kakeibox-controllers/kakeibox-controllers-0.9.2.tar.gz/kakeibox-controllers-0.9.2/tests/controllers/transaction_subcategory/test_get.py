from kakeibox_controllers.controllers.transaction_subcategory.get \
    import TransactionSubcategoryGet
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from tests.utils.json import assert_json_dict


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_get_transaction_subcategory(transaction_subcategory_dict):
    before_execute_test()
    code = transaction_subcategory_dict['code']
    storage = StorageTransactionSubcategory()
    storage.table = {code: transaction_subcategory_dict}
    action = TransactionSubcategoryGet()
    response = action.execute(code)
    assert_json_dict(transaction_subcategory_dict, response)
