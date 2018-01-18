from pact_test.utils.logger import *
from pact_test.constants import FAILED


def is_subset(expected, actual):
    actual_items = actual.items() if actual else {}
    expected_items = expected.items() if expected else {}

    stripped_actual_items = map(strip_whitespaces_after_commas, actual_items)
    stripped_expected_items = map(strip_whitespaces_after_commas, expected_items)

    return all(item in stripped_actual_items for item in stripped_expected_items)


def strip_whitespaces_after_commas(t):
    k = t[0]
    v = t[1].replace(', ', ',') if type(t[1]) is str else t[1]

    return k, v


def build_error_message(section, expected, actual):
    return {
        'actual': actual,
        'status': FAILED,
        'expected': expected,
        'message': section.capitalize() + ' is incorrect'
    }


def is_string(text):
    try:
        return True if (type(text) is str or type(text) is unicode) else False
    except NameError:
        return True if type(text) is str else False


def match_dicts_all_keys_and_values(d1, d2):
    d1_keys = d1.keys()
    d2_keys = d2.keys()

    delete_extra_keys(d1, d2)

    all_keys = set(d2_keys).issubset(set(d1_keys))
    all_values = match_dicts_all_values(d1, d2)

    return all_keys and all_values


def match_dicts_all_values(d1, d2):
    all_values = True
    for (k1, v1), (k2, v2) in zip(sorted(d2.items()), sorted(d1.items())):
        all_values = all_values and (v1 == v2)
    return all_values


def delete_extra_keys(d1, d2):
    extra_keys = list(set(d2.keys()) - set(d1.keys()))
    for extra_key in extra_keys:
        d2.pop(extra_key, None)
    for (k1, v1), (k2, v2) in zip(sorted(d1.items()), sorted(d2.items())):
        if type(v1) is dict and type(v2) is dict:
            delete_extra_keys(v1, v2)
