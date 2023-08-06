from kakeibox_controllers.controllers.transaction_category.update \
    import TransactionCategoryUpdate
from kakeibox_storage_memory.storage import StorageTransactionCategory
from tests.utils.json import assert_json
import json


def before_execute_test():
    storage = StorageTransactionCategory()
    storage.table = {}


def test_update_transaction_category(transaction_category_dict):
    before_execute_test()
    code = transaction_category_dict['code']
    storage = StorageTransactionCategory()
    storage.table = {code: transaction_category_dict}
    action = TransactionCategoryUpdate()
    json_update_input_dict = {"code": code, "transaction_category":
        json.dumps(transaction_category_dict)}
    response = action.execute(**json_update_input_dict)
    assert_json(json_update_input_dict['transaction_category'], response)

