from sys import argv

from syntaxiperror.validates import address


def test_address():
    address(argv[1])


if __name__ == "__main__":
    test_address()
