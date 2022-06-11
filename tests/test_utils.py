import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common/cryptoApp"))
print(sys.path)


from utils import *


def test_hash():
    string = "Hello World"
    print(hashstring.hash_string(string))


if __name__ == '__main__':
    test_hash()
