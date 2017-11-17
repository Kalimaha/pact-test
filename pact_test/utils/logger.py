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
                print('')
                info('Test: ' + test_result.value['test'])
                for result in test_result.value['results']:
                    if type(result.value) is dict:
                        info('  GIVEN ' + result.value['state'] + ' UPON RECEIVING ' + result.value['description'])
                        info('    status: ' + result.value['status'])
                        for test_error in result.value['errors']:
                            if type(test_error) is dict:
                                error('      expected: ' + str(test_error['expected']))
                                error('      actual:   ' + str(test_error['actual']))
                                error('      message:  ' + str(test_error['message']))
                            else:
                                error('      message: ' + str(test_error))
                    else:
                        error('  ' + str(result.value))
    info('')
    info('Goodbye!')
    print('')


def log_providers_test_results(test_results):
    if type(test_results) is Left:
        error(test_results.value)
    else:
        for r in test_results.value:
            print('')
            info('A pact between ' + r['consumer']['name'] + ' and ' + r['provider']['name'])
            for i in r['interactions']:
                if i['status'] == 'FAILED':
                    error('  Given ' + i['providerState'] + ', upon receiving ' + i['description'] + ' from ' + r['consumer']['name'])
                    error('    Status: ' + i['status'])
                    error('    Message: ' + i['message'])
                    error('    Expected: ' + str(i.get('expected')))
                    error('    Actual: ' + str(i.get('actual')))
                else:
                    info('')
                    info('  Given ' + i['providerState'] + ', upon receiving ' + i['description'] + ' from ' + r['consumer']['name'] + ' with:')
                    info('')
                    info('  {')
                    info('    "method": ' + str(i['request']['method']) + ',')
                    info('    "path": ' + str(i['request']['path']) + ',')
                    info('    "query": ' + str(i['request']['query']) + ',')
                    info('    "headers": ' + str(i['request']['headers']) + ',')
                    info('    "body": ' + str(i['request']['body']))
                    info('  }')
                    info('')
                    info('  ' + r['provider']['name'] + ' will respond with: ')
                    info('')
                    info('  {')
                    info('    "status": ' + str(i['response']['status']) + ',')
                    info('    "body": ' + str(i['response']['body']) + ',')
                    info('    "headers": ' + str(i['response']['headers']))
                    info('  }')
                    info('')
