## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
# Copyright (C) 2008-2010 Seek You Too (CQ2) http://www.cq2.nl
# Copyright (C) 2008-2009 Technische Universiteit Delft http://www.tudelft.nl
# Copyright (C) 2017 SURFmarket https://surf.nl
# Copyright (C) 2017 Seecr (Seek You Too B.V.) http://seecr.nl
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
        fp = open(filename, 'w').write(TESTDATA)
        self.language = Language(filename)

    def testNameForCode(self):
        self.assertEquals({'nl': 'Nederlands', 'en':'Dutch'}, self.language.nameForCode('dut'))
        self.assertEquals({'nl': 'Nederlands', 'en':'Dutch'}, self.language.nameForCode(code3='dut'))
        self.assertEquals({'en': 'English', 'nl': 'Engels'}, self.language.nameForCode(code3='eng'))
        self.assertEquals({'nl': 'Nederlands', 'en':'Dutch'}, self.language.nameForCode(code2='nl'))
        self.assertEquals({'en': 'English', 'nl': 'Engels'}, self.language.nameForCode(code2='en'))
        self.assertEquals({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode('XXX'))

    def testWrongUseOfNameForCode(self):
        self.assertEquals({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode())
        self.assertEquals({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode(code2='nl', code3='dut'))
        self.assertEquals({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode(code2='nl', code3='eng'))
        self.assertEquals({'nl': 'Onbekend', 'en':'Unknown'}, self.language.nameForCode(code2='x', code3='x'))

    def testNormalize(self):
        self.assertEquals('dut', self.language.normalize('dut'))
        self.assertEquals('dut', self.language.normalize('nl'))
        self.assertEquals(None, self.language.normalize('XXX'))

        self.language.addNormalizationRule('ned', 'dut')
        self.assertEquals('dut', self.language.normalize('ned'))

    def testUnparsable(self):
        self.assertEquals('XXX', self.language.unparsable('XXX'))
        self.assertEquals(None, self.language.unparsable('dut'))

        self.language.addNormalizationRule('nld', 'dut')
        self.assertEquals(None, self.language.unparsable('nld'))

    def testAsDict(self):
        l = Language.default()
        result = l.asDict(language='nl', codelength='2')
        self.assertEquals('Nederlands', result['nl'])
        result = l.asDict(language='nl', codelength='3')
        self.assertEquals('Nederlands', result['dut'])
        result = l.asDict(language='en', codelength='2')
        self.assertEquals('Dutch', result['nl'])
        result = l.asDict(language='en', codelength='3')
        self.assertEquals('Dutch', result['dut'])
        result = l.asDict(language='en', codelength='3')
        self.assertEquals('Afrikaans', result['afr'])
