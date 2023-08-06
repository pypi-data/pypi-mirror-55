import unittest

from nonsensepy import NonsensePyGen

class TestNonsensePy(unittest.TestCase):

    def test_starts_with_letter(self):
        result = NonsensePyGen.starts_with_letter()
        self.assertTrue(len(result) > 10)

    def test_starts_with_uppercase(self):
        result = NonsensePyGen.starts_with_uppercase()
        self.assertTrue(64 < ord(result[0]) < 91)

    def test_nrandom(self):
        result = NonsensePyGen.nrandom(size=5)
        self.assertTrue(result.isdigit() and len(result) == 5)

    def test_strrandom(self):
        result = NonsensePyGen.strrandom(size=10)
        digits = list(filter(lambda s: s.isdigit(), result))
        self.assertTrue(len(digits) == 0 and len(result) == 10)

    def test_random(self):
        result = NonsensePyGen.strrandom(size=100)
        self.assertTrue(len(result) == 100)

    def test_random_with_given_min(self):
        result = NonsensePyGen.random(min=100)
        self.assertTrue(len(result) >= 100)

    def test_random_with_given_min_max(self):
        result = NonsensePyGen.random(min=100, max=200)
        self.assertTrue(100 <= len(result) <= 200)

    def test_random_raise_exception(self):
        self.assertRaises(ValueError, NonsensePyGen.random, min=100, max=100)