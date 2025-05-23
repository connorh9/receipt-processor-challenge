#!/usr/bin/env python

import unittest
import sys

def run_tests():
    loader = unittest.TestLoader()
    print("\nUnit Tests\n")
    suite = loader.discover('.', pattern='tester.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)