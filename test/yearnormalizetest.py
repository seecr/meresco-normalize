## begin license ##
#
#    Meresco Normalize is an open-source library containing normalization 
#    components for use with Meresco
#
#    Copyright (C) 2008-2009 Universiteit van Tilburg http://www.uvt.nl
#    Copyright (C) 2008-2009 Technische Universiteit Delft http://www.tudelft.nl
#    Copyright (C) 2008-2010 Seek You Too (CQ2) http://www.cq2.nl
#
#    This file is part of Meresco Normalize.
#
#    Meresco Normalize is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    Meresco Normalize is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Meresco Normalize; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
## end license ##
from unittest import TestCase

from meresco.normalize.date import YearNormalize
from normalizetestcase import NormalizeTestCase

class YearNormalizeTest(NormalizeTestCase):
    def setUp(self):
        self.normalize = YearNormalize(yearRange=(1400,2100))

    def testSimpleYear(self):
        self.assertNormalize('2008', '2008')
        self.assertUnparsable('ABCD')

    def testDitchQuestionMarkAtEnd(self):
        self.assertNormalize('2008', '2008?')

    def testSimpleDateBetweenRange(self):
        self.assertNormalize('2008', '2008')
        self.assertNormalize('1400', '1400')
        self.assertNormalize('2100', '2100')
        self.assertUnparsable('0004')
        self.assertUnparsable('1399')
        self.assertUnparsable('2101')

    def testUnparsable(self):
        self.assertUnparsable('Everything else is')
        self.assertUnparsable('unparsable')
        self.assertUnparsable(None)

    def testDateYYYY_MM_DD(self):
        self.assertNormalize('2008', '2008-01-01')
        self.assertNormalize('2007', '2007-12-31')
        self.assertNormalize('2006', '2006-00-00')
        self.assertNormalize('2005', '2005-99-99')
        self.assertUnparsable('2005-1-1')
        self.assertUnparsable('2005-12-1')
        self.assertUnparsable('2005-1-12')

    def testYearLessThanThousand(self):
        self.normalize = YearNormalize(yearRange=(0,2100))
        self.assertNormalize('0008', '0008')

    def testAddRegex(self):
        self.assertUnparsable('[2008]')
        aRegexString = r'^\[(\d{4})\]$'
        self.normalize.addRegex(aRegexString)

        self.assertNormalize('2008', '[2008]')
