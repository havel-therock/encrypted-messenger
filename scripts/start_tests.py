#!/usr/bin/env python3
import os
import sys
import glob
from pathlib import Path
from subprocess import call


def run_test(path):
    if os.path.isfile(path):
        print("file")
        call(["python3", path]) # if problems change python3 --> python
    elif os.path.isdir(path):
        print("dir")
        print(path)
        if path[-1] != "/":
            path += "/"
        list_of_testfiles = glob.glob(path + "test*.py")
        for testfile in list_of_testfiles:
            call(["python3", testfile])  # if problems change python3 --> python


if __name__ == "__main__":
    # SETUP
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cur_path = Path(dir_path)
    sys.path.append(str(cur_path.parent.absolute()))
    # END OF SETUP
    # IMPORTS
    # ...
    # END OF IMPORTS

    # TESTS
    run_test("../tests/component-tests/module1")
    # more tests here...
    # END OF TESTS
