## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
# Copyright (C) 2008-2010 Seek You Too (CQ2) http://www.cq2.nl
# Copyright (C) 2008-2009 Technische Universiteit Delft http://www.tudelft.nl
# Copyright (C) 2017 SURFmarket https://surf.nl
# Copyright (C) 2017, 2020 Seecr (Seek You Too B.V.) https://seecr.nl
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
from os.path import join

from meresco.normalize.language import Language

TESTDATA="""dut\tnl\tNederlands\tDutch
eng\ten\tEngels\tEnglish
ger\tde\tDuits\tGerman
"""

class LanguageTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)
        filename = join(self.tempdir, 'languages.txt')
        with open(filename, 'w') as f: f.write(TESTDATA)
        self.language = Language(filename)

    def testNameForCode(self):
        self.assertEqual({'nl': 'Nederlands', 'en':'Dutch'}, self.language.nameForCode('dut'))
        self.assertEqual({'nl': 'Nederlands', 'en':'Dutch'}, self.language.nameForCode(code3='dut'))
        self.assertEqual({'en': 'English', 'nl': 'Engels'}, self.language.nameForCode(code3='eng'))
        self.assertEqual({'nl': 'Nederlands', 'en':'Dutch'}, self.language.nameForCode(code2='nl'))
        self.assertEqual({'en': 'English', 'nl': 'Engels'}, self.language.nameForCode(code2='en'))
        self.assertEqual({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode('XXX'))

    def testWrongUseOfNameForCode(self):
        self.assertEqual({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode())
        self.assertEqual({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode(code2='nl', code3='dut'))
        self.assertEqual({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode(code2='nl', code3='eng'))
        self.assertEqual({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode(code2='x', code3='x'))

    def testNormalize(self):
        self.assertEqual('dut', self.language.normalize('dut'))
        self.assertEqual('dut', self.language.normalize('nl'))
        self.assertEqual(None, self.language.normalize('XXX'))

        self.language.addNormalizationRule('ned', 'dut')
        self.assertEqual('dut', self.language.normalize('ned'))

    def testUnparsable(self):
        self.assertEqual('XXX', self.language.unparsable('XXX'))
        self.assertEqual(None, self.language.unparsable('dut'))

        self.language.addNormalizationRule('nld', 'dut')
        self.assertEqual(None, self.language.unparsable('nld'))

    def testAsDict(self):
        l = Language.default()
        result = l.asDict(language='nl', codelength='2')
        self.assertEqual('Nederlands', result['nl'])
        result = l.asDict(language='nl', codelength='3')
        self.assertEqual('Nederlands', result['dut'])
        result = l.asDict(language='en', codelength='2')
        self.assertEqual('Dutch', result['nl'])
        result = l.asDict(language='en', codelength='3')
        self.assertEqual('Dutch', result['dut'])
        result = l.asDict(language='en', codelength='3')
        self.assertEqual('Afrikaans', result['afr'])
