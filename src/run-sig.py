#!/usr/bin/env python3

# NOTE:  This startup script is here for demonstration.  Consider using
#
#       python3 -m sig
#
#   instead of
#
#       ./run-sig.py
#
# NOTE:  With Setuptools the package can be configured for installation
#   with pip so that installing the package will automatically generate
#   and install a platform-specific startup executable.

from sig.cli import main
from sys import argv
# NOTE: `exit` already means something in Python
from sys import exit as sys_exit

sys_exit(main(argv[1:]))
