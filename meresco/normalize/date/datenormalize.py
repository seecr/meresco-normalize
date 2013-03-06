## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
# Copyright (C) 2008-2010 Seek You Too (CQ2) http://www.cq2.nl
# Copyright (C) 2008-2009 Technische Universiteit Delft http://www.tudelft.nl
# Copyright (C) 2008-2009 Universiteit van Tilburg http://www.uvt.nl
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

from re import compile

class DateNormalize(object):
    def __init__(self, format="YYYY", yearRange=(1400, 2100)):
        self._yearBottom, self._yearTop = yearRange

        self._regExp = regExps[format]
        if '-' in format:
            self._postprocess = lambda result: result
        else:
            self._postprocess = lambda result: result.replace('-', '')

    def normalize(self, aString):
        for yearRe in self._regExp:
            result = self._normalize(aString, yearRe)
            if result != None:
                return self._postprocess(result)
        return None

    def unparsable(self, aString):
        return aString if self.normalize(aString) is None else None

    def addRegex(self, aRegexString):
        assert '(?P<year>' in aRegexString
        self._regExp.append(compile(aRegexString))

    def _normalize(self, aString, yearRe):
        try:
            match = yearRe.match(aString)
            if match and self._yearBottom <= int(match.groupdict()['year']) <= self._yearTop:
                return match.group(1)
        except TypeError:
            return None

regExps = {
    "YYYY": [
        compile(r'^((?P<year>\d{4}))$'), #2008
        compile(r'^((?P<year>\d{4}))\?$'), #2008?
        compile(r'^((?P<year>\d{4}))-\d{2}-\d{2}$'), #2008-01-01
        compile(r'^((?P<year>\d{4}))-\d{2}$'), #2008-01
    ],
    "YYYY-MM": [
        compile(r'^((?P<year>\d{4})-\d{2})-\d{2}$'), #2008-01-01
        compile(r'^((?P<year>\d{4})-\d{2})$'), #2008-01
    ],
    "YYYY-MM-DD": [
        compile(r'^((?P<year>\d{4})-\d{2}-\d{2})$'), #2008-01-01
    ]
}
regExps['YYYYMMDD'] = regExps['YYYY-MM-DD']
regExps['YYYYMM'] = regExps['YYYY-MM']
