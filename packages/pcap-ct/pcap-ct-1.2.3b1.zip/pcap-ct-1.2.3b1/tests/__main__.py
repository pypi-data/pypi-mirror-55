# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# https://opensource.org/licenses/BSD-3-Clause/

import unittest
import sys
import os
import logging

from . import test_dir


def test_suite(names=None, omit=("test", "testsniff")):
    from . import __name__ as pkg_name
    from . import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name != "__main__" and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def main(argv=sys.argv):
    print("Running tests", "\n", file=sys.stderr)
    tests = test_suite(argv[1:] or None)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__.rpartition(".")[-1] == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    main()
