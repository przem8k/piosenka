import doctest

from songs import transpose


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(transpose))
    return tests
