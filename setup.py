#!/usr/bin/env python3
## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
# Copyright (C) 2010 Seek You Too (CQ2) http://www.cq2.nl
# Copyright (C) 2020-2021 Data Archiving and Network Services https://dans.knaw.nl
# Copyright (C) 2020-2021 SURF https://www.surf.nl
# Copyright (C) 2020-2021 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2020-2021 Stichting Kennisnet https://www.kennisnet.nl
# Copyright (C) 2020-2021 The Netherlands Institute for Sound and Vision https://beeldengeluid.nl
#
# This file is part of "Meresco Normalize"
#
# "Meresco Normalize" is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# "Meresco Normalize" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with "Meresco Normalize"; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
## end license ##

from distutils.core import setup
from os import walk
from os.path import join

version = '$Version: 0$'[9:-1].strip()

data_files = []
for path, dirs, files in walk('usr-share'):
    data_files.append((path.replace('usr-share', '/usr/share/meresco-normalize', 1), [join(path, f) for f in files]))

packages = []
for path, dirs, files in walk('meresco'):
    if '__init__.py' in files and path != 'meresco':
        packages.append(path.replace('/', '.'))

setup(
    name='meresco-normalize',
    packages = [
        'meresco',                          #DO_NOT_DISTRIBUTE
    ] + packages,
    data_files=data_files,
    version=version,
    url='http://www.meresco.org',
    author='Seek You Too',
    author_email='info@cq2.nl',
    description='Meresco Normalize is an open-source library containing normalization components for use with Meresco',
    long_description='Meresco Normalize is an open-source library containing normalization components for use with Meresco',
    license='GNU Public License',
    platforms='all',
)
