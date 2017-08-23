import os
import json


def load_acceptance_test(path_to_file):
    acceptance_test_filename = os.path.basename(path_to_file).split('.py')[0]
    acceptance_test_filename += '.json'
    dir_name = os.path.dirname(path_to_file)

    path = os.path.join(dir_name, acceptance_test_filename)
    with open(path) as f:
        data = json.load(f)

    return data
