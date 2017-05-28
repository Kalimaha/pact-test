__all__ = ['Either', 'Left', 'Right']


class Either(object):
    def __init__(self, value):
        self.value = value

    def concat(self, f, *args):
        if type(self) is Right:
            return f(self.value, *args)
        else:
            return self


class Left(Either):
    pass


class Right(Either):
    pass
