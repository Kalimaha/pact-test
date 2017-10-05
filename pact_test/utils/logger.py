from pact_test.either import *

PREFIX = '[Pact Test for Python] - '                        # pragma: no cover


def info(message):                                          # pragma: no cover
    print('\033[92m' + PREFIX + str(message) + '\033[0m')   # pragma: no cover


def error(message):                                         # pragma: no cover
    print('\033[91m' + PREFIX + str(message) + '\033[0m')   # pragma: no cover


def debug(message):                                         # pragma: no cover
    print('\033[93m' + PREFIX + str(message) + '\033[0m')   # pragma: no cover


def log_consumers_test_results(test_results):
    if type(test_results) is Left:
        error(test_results.value)
    else:
        if type(test_results.value) is Left:
            error(test_results.value.value)
        else:
            for test_result in test_results.value:
                print()
                info('Test: ' + test_result.value['test'])
                for result in test_result.value['results']:
                    info('  GIVEN ' + result.value['state'] + ' UPON RECEIVING ' + result.value['description'])
                    info('    status: ' + result.value['status'])
                    for test_error in result.value['errors']:
                        error('      expected: ' + str(test_error['expected']))
                        error('      actual:   ' + str(test_error['actual']))
                        error('      message:  ' + str(test_error['message']))
    info('')
    info('Goodbye!')
    print()


def log_providers_test_results(test_results):
    print(test_results)
