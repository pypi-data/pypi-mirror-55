from kakeibox_controllers.controllers.transaction_category.get \
    import TransactionCategoryGet
from kakeibox_storage_memory.storage import StorageTransactionCategory
from tests.utils.json import assert_json_dict


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_get_transaction_category(transaction_category_dict):
    before_execute_test()
    code = transaction_category_dict['code']
    storage = StorageTransactionCategory()
    storage.table = {code: transaction_category_dict}
    action = TransactionCategoryGet()
    response = action.execute(code)
    assert_json_dict(transaction_category_dict, response)
