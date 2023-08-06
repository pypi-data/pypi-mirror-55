import sys

if sys.version_info != (2, 7) or sys.version_info < (3, 7):
    raise AssertionError("The required version of python is >= 3.7")
