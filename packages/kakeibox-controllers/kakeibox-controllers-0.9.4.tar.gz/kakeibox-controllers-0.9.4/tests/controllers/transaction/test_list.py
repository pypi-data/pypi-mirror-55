from kakeibox_controllers.controllers.transaction.list \
    import TransactionList
from kakeibox_storage_memory.storage import StorageTransaction
from tests.utils.json import assert_json_list
import datetime
import json


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def test_list_transaction(transaction_data):
    before_execute_test()
    storage = StorageTransaction()
    storage.table = transaction_data
    start_time = datetime.datetime(2019, 1, 1, 0, 0, 0).timestamp()
    end_time = datetime.datetime.now().timestamp()
    input_dict = dict(
        start_time=start_time,
        end_time=end_time,
    )

    action = TransactionList()
    response = action.execute(json.dumps(input_dict))
    assert_json_list(transaction_data, response)
