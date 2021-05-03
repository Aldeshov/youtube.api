import random
import string


def random_code(length=16):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def random_key(length=8):
    start = 10 ** (length - 1)
    end = (10 ** length) - 1
    return random.randint(start, end)
