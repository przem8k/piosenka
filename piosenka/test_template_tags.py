import doctest

from piosenka.templatetags import list_partition


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(list_partition))
    return tests
