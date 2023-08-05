import random
from random import randint
from random import shuffle


class NonsensePyGen:

    STR = "ABCDEFJHIGKLMNOPQRSTUVWXYZ0123456789abcdefjhijklmnopqrstuvwxyz"
    DIGITS = "0123456789"
    LETTERS = "ABCDEFJHIGKLMNOPQRSTUVWXYZabcdefjhijklmnopqrstuvwxyz"
    ULETTERS = "ABCDEFJHIGKLMNOPQRSTUVWXYZ"

    MIN = 10
    MAX = 10000

    @staticmethod
    def _random(**kwargs):
        random.seed()
        size = (
            kwargs["size"]
            if "size" in kwargs
            else randint(NonsensePyGen.MIN, NonsensePyGen.MAX)
        )

        rand = [
            NonsensePyGen.STR[randint(0, len(NonsensePyGen.STR) - 1)]
            for _ in range(size)
        ]
        return rand

    @staticmethod
    def starts_with_letter(**kwargs):
        rand = NonsensePyGen._random(**kwargs)

        letter = NonsensePyGen.LETTERS[randint(0, len(NonsensePyGen.LETTERS) - 1)]
        rand[0] = letter
        return "".join(rand)

    @staticmethod
    def starts_with_digit(**kwargs):
        rand = NonsensePyGen._random(**kwargs)

        digit = NonsensePyGen.DIGITS[randint(0, len(NonsensePyGen.DIGITS) - 1)]

        rand[0] = digit
        return "".join(rand)

    @staticmethod
    def starts_with_uppercase(**kwargs):
        rand = NonsensePyGen._random(**kwargs)

        letter = NonsensePyGen.ULETTERS[randint(0, len(NonsensePyGen.ULETTERS) - 1)]
        rand[0] = letter
        return "".join(rand)

    @staticmethod
    def random(**kwargs):
        rand = NonsensePyGen._random(**kwargs)
        return "".join(rand)

    @staticmethod
    def nrandom(**kwargs):
        random.seed()
        size = (
            kwargs["size"]
            if "size" in kwargs
            else randint(NonsensePyGen.MIN, NonsensePyGen.MAX)
        )
        rand = [
            NonsensePyGen.DIGITS[randint(0, len(NonsensePyGen.DIGITS) - 1)]
            for _ in range(size)
        ]
        return "".join(rand)

    @staticmethod
    def strrandom(**kwargs):
        random.seed()
        size = (
            kwargs["size"]
            if "size" in kwargs
            else randint(NonsensePyGen.MIN, NonsensePyGen.MAX)
        )
        rand = [
            NonsensePyGen.LETTERS[randint(0, len(NonsensePyGen.LETTERS) - 1)]
            for _ in range(size)
        ]
        return "".join(rand)
