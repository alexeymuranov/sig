#!/usr/bin/env python3

from setuptools import setup, find_packages

root_dir = 'src'
app_name = 'sig'
# NOTE:  The "version" declared here is the same as `sig.__version__`.
#   However, it seems unreasonable to try to define it in just one place
#   and to have imported elsewhere through various tricks.  In particular,
#   importing a module into its own installation script would probably be
#   a bad ("circular") design.
app_version = '0.1b0.dev0'

setup(  name = app_name,
        version = app_version,

        package_dir = {'': root_dir},
        packages = find_packages(root_dir),
        entry_points = {'console_scripts': [
                '{0} = {0}._extra_api_for_setuptools:main_entry_point'
                .format(app_name) ]},

        include_package_data = True,

        zip_safe = True,

        install_requires = [ 'numpy >= 1.10, < 2',
                             'scipy >= 0.17, < 2',
                             'sympy >= 1, < 2' ],

        author = 'Alexey Muranov',
        author_email = 'alexeymuranov@users.noreply.github.com',
        description = 'Read some input, generate some matrices, '
                'compute their signatures, select "interesting" '
                'signatures, print them out.',
        url = 'https://github.com/alexeymuranov/sig' )
