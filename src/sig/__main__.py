# The file named "__main__.py" in a module (package) is executed when Python
# is asked to "execute" the containing module (package) with
#
#     python3 -m <module name>
#
# Thus this is the main "startup script" for the parent module (package).
# This script can be bypassed by declaring "entry points" with Setuptools
# and installing the package (project) with pip, in which case platform-
# specific startup executables will be automatically created and installed.
#
# This file can be easily converted into a startup script that can be run
# directly: it is enough to move or copy it to the directory containing the
# parent module (package), possibly renaming it, and to replace all relative
# imports with absolute ones.  Of course, if the parent module (package) is
# installed so that Python can find it, then the startup script can be
# placed anywhere.
#
# NOTE: this script will fail if executed directly because relative
#   imports expect the parent module (package) to have been already loaded
#   (maybe for other obscure reasons too)

from sys import argv
# NOTE: `exit` already means something in Python
from sys import exit as sys_exit
from .cli import main

# NOTE: `sys.exit` is useless here if `main` calls it anyway, but
#   harmless and normally expected
sys_exit(main(argv))
