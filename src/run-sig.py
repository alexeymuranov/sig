#!/usr/bin/env python3

# -----------------------------------
# Startup script based on __main__.py
# -----------------------------------
#
# This startup script is here for demonstration.  Consider using
#
#     python3 -m sig
#
# instead of
#
#     ./run-sig.py
#
# NOTE:  With Setuptools the package can be configured for installation
#   with pip so that installing the package will automatically generate
#   and install a platform-specific startup executable.

from sys import argv
# NOTE: `exit` already means something in Python
from sys import exit as sys_exit
from sig.cli import main

# NOTE: `sys.exit` is useless here if `main` calls it anyway, but
#   harmless and normally expected
sys_exit(main(argv[1:]))
