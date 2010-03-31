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
from meresconormalize.name import FirstInitialNormalize, LastnameNormalize
from normalizetestcase import NormalizeTestCase

class NormalizeWrapperTest(NormalizeTestCase):

    def testNameNormalize(self):
        self.normalize = FirstInitialNormalize()

        self.assertNormalize("Peters, H.", "Peters, H.")
        self.assertNormalize("Peters, H.", "Peters, H.J.M.")
        self.assertNormalize("Peters, H.", "Peters, H. J. M.")
        self.assertNormalize("Guillen Scholten, J.", "Guillen Scholten, J. V.")
        self.assertNormalize("Peters, H.", "Peters, Hans")
        self.assertNormalize("Peters, H.", "Peters, H")
        self.assertNormalize("Peters, H.", "Peters, H. (Hans)")
        self.assertNormalize("Peters, H.", "Peters, H.J.M. (Hans)")
        self.assertNormalize("Peters, H.", "Peters, H. (Hans Jan Marie)")
        self.assertNormalize("Peters, H.", "Peters, HJM")
        self.assertNormalize("Peters, H.", "Peters, Hans Jan Marie")
        self.assertNormalize("Peters, J.", "Peters, J.-J.")
        self.assertNormalize("Peters, J.", "Peters, J-J.")
        self.assertNormalize("Beaumont, W.", "Beaumont, W.Worby")
        self.assertNormalize("Berg, P. v.d.", "Berg, P.J. van den")
        self.assertNormalize("Genn, R.", 'Genn, R.C. (Jr.)')
        self.assertNormalize("Petri, N.", "Petri, Nicolaus (Daventriensis)")

        self.assertUnparsable('this is not a valid name?')
        #self.assertUnparsable("ASTM Committee D-2 on Petroleum Products and Lubricants")

    def testLastnameNormalize(self):
        self.normalize = LastnameNormalize()
        self.assertNormalize("Peters", "Peters, H.")
        self.assertNormalize("Peters", "Peters, H.J.M.")
        self.assertNormalize("Peters", "Peters, H. J. M.")
        self.assertNormalize("Guillen Scholten", "Guillen Scholten, J. V.")
        self.assertNormalize("Peters", "Peters, Hans")
        self.assertNormalize("Peters", "Peters, H")
        self.assertNormalize("Peters", "Peters, H. (Hans)")
        self.assertNormalize("Peters", "Peters, H.J.M. (Hans)")
        self.assertNormalize("Peters", "Peters, H. (Hans Jan Marie)")
        self.assertNormalize("Peters", "Peters, HJM")
        self.assertNormalize("Peters", "Peters, Hans Jan Marie")
        self.assertNormalize("Peters", "Peters, J.-J.")
        self.assertNormalize("Peters", "Peters, J-J.")
        self.assertNormalize("Beaumont", "Beaumont, W.Worby")
        self.assertNormalize("Berg, v.d.", "Berg, P.J. van den")
        self.assertNormalize("Genn", 'Genn, R.C. (Jr.)')
        self.assertNormalize("Petri", "Petri, Nicolaus (Daventriensis)")

        self.assertUnparsable('this is not a valid name?')
        #self.assertUnparsable("ASTM Committee D-2 on Petroleum Products and Lubricants")
