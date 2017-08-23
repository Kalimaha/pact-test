PREFIX = '[Pact Test for Python] - '                        # pragma: no cover


def info(message):                                          # pragma: no cover
    print('\033[92m' + PREFIX + message + '\033[0m')        # pragma: no cover


def error(message):                                         # pragma: no cover
    print('\033[91m' + PREFIX + message + '\033[0m')        # pragma: no cover
