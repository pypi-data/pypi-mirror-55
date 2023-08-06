from kakeibox_controllers.controllers.transaction_subcategory\
    .list_per_category import TransactionSubcategoryListPerCategory
from kakeibox_storage_memory.storage import StorageTransactionSubcategory
from tests.utils.json import assert_json_dict


def before_execute_test():
    storage = StorageTransactionSubcategory()
    storage.table = {}


def _get_category_subcategories(storage, category):
    return [item for item in storage.table.values()
            if item['transaction_category_code'] == category
            ]


def _assert_list_per_category(storage, category):
    transaction_subcategories = _get_category_subcategories(storage, category)
    action = TransactionSubcategoryListPerCategory()
    response = action.execute(category)
    assert_json_dict(transaction_subcategories, response)


def test_list_transaction_category(transaction_subcategory_data,
                                   transaction_category_data):
    before_execute_test()
    storage = StorageTransactionSubcategory()
    storage.table = transaction_subcategory_data

    for transaction_category in transaction_category_data.values():
        category = transaction_category['code']
        _assert_list_per_category(storage, category)
