import random
import string


def getRandomString(self, size=6, chars=string.ascii_uppercase+string.digits):
    return ''.join(random.choices(chars, k=size))

