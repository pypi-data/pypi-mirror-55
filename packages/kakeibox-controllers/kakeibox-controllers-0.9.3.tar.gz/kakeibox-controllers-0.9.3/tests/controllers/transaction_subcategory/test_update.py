from kakeibox_controllers.controllers.transaction_subcategory.update \
    import TransactionSubcategoryUpdate
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from tests.utils.json import assert_json
import json


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def test_update_transaction_subcategory(transaction_subcategory_dict):
    before_execute_test()
    code = transaction_subcategory_dict['code']
    storage = StorageTransactionSubcategory()
    storage.table = {code: transaction_subcategory_dict}

    json_update_subcategory_input_dict = {"code": code,
                                          "transaction_subcategory":
        json.dumps(transaction_subcategory_dict)}

    action = TransactionSubcategoryUpdate()
    response = action.execute(**json_update_subcategory_input_dict)
    assert_json(json_update_subcategory_input_dict['transaction_subcategory'],
                response)
