import doctest

from piosenka import lyrics


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(lyrics))
    return tests
