## begin license ##
#
#    Meresco Normalize is an open-source library containing normalization 
#    components for use with Meresco
#
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

class Language(object):
    def __init__(self, languageFile):
        parsedFile = list(parts for parts in (line.strip().split('\t')
            for line in open(languageFile)))

        self._languages = dict((code3, {'nl': dutch, 'en': english})
            for code3, code2, dutch, english in parsedFile)

        self._normalizations = dict((code2, code3)
            for code3, code2, dutch, english in parsedFile)

    def nameForCode(self, code3):
        return self._languages.get(code3, {'nl': 'Onbekend', 'en':'Unknown'})

    def normalize(self, aLanguage):
        language = self._normalizations.get(aLanguage, aLanguage)

        if language in self._languages:
            return language

    def addNormalizationRule(self, aValue, languageCode3):
        self._normalizations[aValue] = languageCode3

    def unparsable(self, aLanguage):
        if not self.normalize(aLanguage):
            return aLanguage
