## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
# Copyright (C) 2013 Seecr (Seek You Too B.V.) http://seecr.nl
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

from meresco.normalize.date import DateNormalize
from normalizetestcase import NormalizeTestCase

class DateNormalizeYearMonthTest(NormalizeTestCase):
    def setUp(self):
        self.normalize = DateNormalize(format="YYYY-MM", yearRange=(1400,2100))

    def testSimpleYear(self):
        self.assertUnparsable('2008')
        self.assertUnparsable('ABCD')

    def testUnparsable(self):
        self.assertUnparsable('Everything else is')
        self.assertUnparsable('unparsable')
        self.assertUnparsable(None)

    def testDateYYYY_MM_DD(self):
        self.assertNormalize('2008-01', '2008-01-01')
        self.assertNormalize('2007-12', '2007-12-31')
        self.assertNormalize('2006-00', '2006-00-00')
        self.assertNormalize('2005-99', '2005-99-99')
        self.assertUnparsable('2005-1-1')
        self.assertUnparsable('2005-12-1')
        self.assertUnparsable('2005-1-12')

    def testDateYYYY_MM(self):
        self.assertNormalize('2008-01', '2008-01')
        self.assertNormalize('2007-12', '2007-12')

    def testDateYYYYMM(self):
        self.normalize = DateNormalize(format="YYYYMM", yearRange=(1400,2100))
        self.assertNormalize('200801', '2008-01')
        self.assertNormalize('200712', '2007-12')

    def testAddRegex(self):
        self.assertUnparsable('[2008]')
        aRegexString = r'^\[((?P<year>\d{4})-\d{2})-\d{2}\]$'
        self.normalize.addRegex(aRegexString)

        self.assertNormalize('2008-04', '[2008-04-05]')
