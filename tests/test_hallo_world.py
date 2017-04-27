import unittest
from pypact.hallo_world import func


class TestHalloWorld(unittest.TestCase):

    def test_answer(self):
        assert func(3) == 5