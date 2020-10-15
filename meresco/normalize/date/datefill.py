## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
# Copyright (C) 2018, 2020 Seecr (Seek You Too B.V.) https://seecr.nl
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

from seecr.zulutime import ZuluTime, TimeError

class DateFill(object):
    @classmethod
    def toBeginning(cls):
        """Will fill dates to full ZuluTime assuming the beginning of missing parts.

- No month: choose 01
- No day: choose 01
- No hour: choose 00 
- No minute/second: choose 00
- No timezone: choose zulu

Examples:
2018-10-25T14:11:34Z -> 2018-10-25T14:11:34Z
2018-10-25T14:11:34 -> 2018-10-25T14:11:34Z
2018-10-25T16:11:34+02:00 -> 2018-10-25T14:11:34Z
2018-10-25T01:11:34+02:00 -> 2018-10-24T23:11:34Z
2018-10-25T01:11 -> 2018-10-25T01:11:00Z
2018-10-25T01 -> 2018-10-25T01:00:00Z
2018-10-25 -> 2018-10-25T00:00:00Z
2018-10 -> 2018-10-01T00:00:00Z
2018 -> 2018-01-01T00:00:00Z
"""
        r = cls()
        r._strategy = _ToBeginningStrategy()
        return r

    @classmethod
    def toHalfway(cls):
        """Will fill dates to full ZuluTime assuming the halfway of missing parts.

- No month: choose 07
- No day: choose 01
- No hour: choose 12
- No minute/second: choose 00
- No timezone: choose zulu

Examples:
2018-10-25T14:11:34Z -> 2018-10-25T14:11:34Z
2018-10-25T14:11:34 -> 2018-10-25T14:11:34Z
2018-10-25T16:11:34+02:00 -> 2018-10-25T14:11:34Z
2018-10-25T01:11:34+02:00 -> 2018-10-24T23:11:34Z
2018-10-25T01:11 -> 2018-10-25T01:11:00Z
2018-10-25T01 -> 2018-10-25T01:00:00Z
2018-10-25 -> 2018-10-25T12:00:00Z
2018-10 -> 2018-10-01T12:00:00Z
2018 -> 2018-07-01T12:00:00Z
"""
        r = cls()
        r._strategy = _ToHalfwayStrategy()
        return r

    def normalize(self, value):
        return self._strategy(value).zulu()

    def normalizeToEpoch(self, value):
        return self._strategy(value).epoch


class _ToBeginningStrategy(object):
    def __call__(self, value):
        try:
            return ZuluTime(value)
        except TimeError as e:
            raise ValueError(e)

class _ToHalfwayStrategy(object):
    def __call__(self, value):
        try:
            result = ZuluTime(value)
            if len(value) <= len('YEAR'):
                result = result.add(months=6)
            if len(value) <= len('YEAR-MM-DDT'):
                result = result.add(hours=12)
            return result
        except TimeError as e:
            raise ValueError(e)
