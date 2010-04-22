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
from namenormalize import lastnameAndFirstInitial, lastname

class NormalizeWrapper(object):
    def unparsable(self, name):
        if not self.normalize(name):
            return name
        return None
    
    def normalize(self, name):
        try:
            return self._normalize(name).next()
        except StopIteration:
            return None
        
class FirstInitialNormalize(NormalizeWrapper):
    def _normalize(self, name):
        return lastnameAndFirstInitial(name)

class LastnameNormalize(NormalizeWrapper):
    def _normalize(self, name):
        return lastname(name)

