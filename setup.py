# Copyright (C) 2012-2017 by the Free Software Foundation, Inc.
#
# This file is part of Postorius.
#
# Postorius is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Postorius is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Postorius.  If not, see <http://www.gnu.org/licenses/>.

import re
import sys
from setuptools import setup, find_packages

# Calculate the version number without importing the postorius package.
with open('src/postorius/__init__.py') as fp:
    for line in fp:
        mo = re.match("__version__ = '(?P<version>[^']+?)'", line)
        if mo:
            __version__ = mo.group('version')
            break
    else:
        print('No version number found')
        sys.exit(1)


setup(
    name="postorius",
    version=__version__,
    description="A web user interface for GNU Mailman",
    long_description=open('README.rst').read(),
    maintainer="The Mailman GSOC Coders",
    license='GPLv3',
    keywords='email mailman django',
    url=" https://gitlab.com/mailman/postorius",
    classifiers=[
        "Programming Language :: Python",
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Django>=1.8,<1.12',
        'django-mailman3',
        'mailmanclient~=3.1.1a1'
    ],
    tests_require=[
        "mock",
        "vcrpy",
        "beautifulsoup4",
    ],
)
