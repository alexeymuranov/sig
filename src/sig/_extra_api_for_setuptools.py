# The function defined in this module shall only be used by Setuptools as
# a "console script entry point."  The problem it solves is that for some
# reason Setuptools can only create startup executables that run "entry
# point" functions without arguments.
from sys import argv
from .cli import main


def main_entry_point():
    return main(argv[1:])
