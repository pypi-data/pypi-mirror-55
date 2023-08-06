import json


def assert_json(expected, result):
    expected_dict = json.loads(expected)
    result_dict = json.loads(result)
    assert expected_dict == result_dict


def assert_json_dict(expected_dict, result):
    result_dict = json.loads(result)
    assert expected_dict == result_dict


def assert_json_list(expected_dict, result_str):
    result_dict = json.loads(result_str)
    assert list(expected_dict.values()) == result_dict

    assert isinstance(result_dict, list)
    for element in result_dict:
        assert isinstance(element, dict)
