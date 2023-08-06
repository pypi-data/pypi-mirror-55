from kakeibox_controllers.controllers.expense.total import ExpenseTotal
from kakeibox_storage_memory.storage import StorageTransaction
import datetime
import json


def before_execute_test():
    storage = StorageTransaction()
    storage.table = {}


def _get_expected_total(items, start_time, end_time):
    incomes = [
        item for item in items
        if int(start_time) <= int(item['timestamp']) <= int(end_time)
           and item['transaction_type_code'] == 'EXP'
    ]
    total_income = 0
    for income in incomes:
        total_income += income['amount']
    return round(total_income, 2)


def test_list_expenses(transaction_data):
    before_execute_test()
    start_time = datetime.datetime(2019, 1, 1, 0, 0, 0).timestamp()
    end_time = datetime.datetime.now().timestamp()
    input_dict = dict(
        start_time=start_time,
        end_time=end_time,
    )
    storage = StorageTransaction()
    storage.table = transaction_data
    total_expected = _get_expected_total(storage.table.values(), start_time,
                                         end_time)

    action = ExpenseTotal()
    response = action.execute(json.dumps(input_dict))
    assert total_expected == float(response)
