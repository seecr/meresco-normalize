## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
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

from seecr.test import SeecrTestCase
from seecr.zulutime import ZuluTime

from meresco.normalize.date import DateFill

class DateFillTest(SeecrTestCase):
    def testBeginningStrategyEpoch(self):
        normalize = DateFill.toBeginning().normalizeToEpoch
        self.assertEqual(1540998692, normalize('2018-10-31T15:11:32Z'))
        self.assertEqual(1540998692, normalize('2018-10-31T16:11:32+01:00'))
        self.assertEqual(1529943092, normalize('2018-06-25T16:11:32Z'))
        self.assertEqual(1529943092, normalize('2018-06-25T18:11:32+02:00'))
        self.assertEqual(1529943092, normalize('2018-06-25T16:11:32.6Z'))
        self.assertEqual(ZuluTime('2018-06-25T16:11:32Z').epoch, normalize('2018-06-25T16:11:32'))
        self.assertEqual(ZuluTime('2018-06-25T16:11:00Z').epoch, normalize('2018-06-25T16:11'))
        self.assertEqual(ZuluTime('2018-06-25T16:00:00Z').epoch, normalize('2018-06-25T16'))
        self.assertEqual(ZuluTime('2018-06-25T00:00:00Z').epoch, normalize('2018-06-25'))
        self.assertEqual(ZuluTime('2018-06-01T00:00:00Z').epoch, normalize('2018-06'))
        self.assertEqual(ZuluTime('2018-01-01T00:00:00Z').epoch, normalize('2018'))

        self.assertRaises(ValueError, lambda: normalize('ooit'))

    def testBeginningStrategyZulu(self):
        normalize = DateFill.toBeginning().normalize
        self.assertEqual('2018-10-31T15:11:32Z', normalize('2018-10-31T15:11:32Z'))
        self.assertEqual('2018-10-31T15:11:32Z', normalize('2018-10-31T16:11:32+01:00'))
        self.assertEqual('2018-06-25T16:11:32Z', normalize('2018-06-25T16:11:32Z'))
        self.assertEqual('2018-06-25T16:11:32Z', normalize('2018-06-25T18:11:32+02:00'))
        self.assertEqual('2018-06-25T16:11:32Z', normalize('2018-06-25T16:11:32.6Z'))
        self.assertEqual('2018-06-25T16:11:32Z', normalize('2018-06-25T16:11:32'))
        self.assertEqual('2018-06-25T16:11:00Z', normalize('2018-06-25T16:11'))
        self.assertEqual('2018-06-25T16:00:00Z', normalize('2018-06-25T16'))
        self.assertEqual('2018-06-25T00:00:00Z', normalize('2018-06-25'))
        self.assertEqual('2018-06-01T00:00:00Z', normalize('2018-06'))
        self.assertEqual('2018-01-01T00:00:00Z', normalize('2018'))

        self.assertRaises(ValueError, lambda: normalize('ooit'))

    def testHalfwayStrategyEpoch(self):
        normalize = DateFill.toHalfway().normalizeToEpoch
        self.assertEqual(1540998692, normalize('2018-10-31T15:11:32Z'))
        self.assertEqual(1540998692, normalize('2018-10-31T16:11:32+01:00'))
        self.assertEqual(1529943092, normalize('2018-06-25T16:11:32Z'))
        self.assertEqual(1529943092, normalize('2018-06-25T18:11:32+02:00'))
        self.assertEqual(1529943092, normalize('2018-06-25T16:11:32.6Z'))
        self.assertEqual(ZuluTime('2018-06-25T16:11:32Z').epoch, normalize('2018-06-25T16:11:32'))
        self.assertEqual(ZuluTime('2018-06-25T16:11:00Z').epoch, normalize('2018-06-25T16:11'))
        self.assertEqual(ZuluTime('2018-06-25T16:00:00Z').epoch, normalize('2018-06-25T16'))
        self.assertEqual(ZuluTime('2018-06-25T12:00:00Z').epoch, normalize('2018-06-25'))
        self.assertEqual(ZuluTime('2018-06-01T12:00:00Z').epoch, normalize('2018-06'))
        self.assertEqual(ZuluTime('2018-07-01T12:00:00Z').epoch, normalize('2018'))

        self.assertRaises(ValueError, lambda: normalize('ooit'))

    def testHalfwayStrategyZulu(self):
        normalize = DateFill.toHalfway().normalize
        self.assertEqual('2018-10-31T15:11:32Z', normalize('2018-10-31T15:11:32Z'))
        self.assertEqual('2018-10-31T15:11:32Z', normalize('2018-10-31T16:11:32+01:00'))
        self.assertEqual('2018-06-25T16:11:32Z', normalize('2018-06-25T16:11:32Z'))
        self.assertEqual('2018-06-25T16:11:32Z', normalize('2018-06-25T18:11:32+02:00'))
        self.assertEqual('2018-06-25T16:11:32Z', normalize('2018-06-25T16:11:32.6Z'))
        self.assertEqual('2018-06-25T16:11:32Z', normalize('2018-06-25T16:11:32'))
        self.assertEqual('2018-06-25T16:11:00Z', normalize('2018-06-25T16:11'))
        self.assertEqual('2018-06-25T16:00:00Z', normalize('2018-06-25T16'))
        self.assertEqual('2018-06-25T12:00:00Z', normalize('2018-06-25'))
        self.assertEqual('2018-06-01T12:00:00Z', normalize('2018-06'))
        self.assertEqual('2018-07-01T12:00:00Z', normalize('2018'))

        self.assertRaises(ValueError, lambda: normalize('ooit'))
