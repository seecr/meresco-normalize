## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
# Copyright (C) 2010 Seek You Too (CQ2) http://www.cq2.nl
# Copyright (C) 2018 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2018 Stichting Kennisnet https://www.kennisnet.nl
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

from seecrdeps import includeParentAndDeps, cleanup     #DO_NOT_DISTRIBUTE
includeParentAndDeps(__file__)                          #DO_NOT_DISTRIBUTE
cleanup(__file__)                                       #DO_NOT_DISTRIBUTE

import unittest

from languagetest import LanguageTest
from namenormalizetest import NameNormalizeTest
from normalizewrappertest import NormalizeWrapperTest
from datenormalizeyeartest import DateNormalizeYearTest
from datenormalizeyearmonthtest import DateNormalizeYearMonthTest
from datenormalizeyearmonthdaytest import DateNormalizeYearMonthDayTest
from datefilltest import DateFillTest

if __name__ == '__main__':
    unittest.main()
