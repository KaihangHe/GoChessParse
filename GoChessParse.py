import os
import click
import unittest
from app import create_app

if __name__ == '__main__':

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
