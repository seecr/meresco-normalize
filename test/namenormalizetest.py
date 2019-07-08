# This Python file uses the following encoding: utf-8
## begin license ##
#
# Meresco Normalize is an open-source library containing normalization
# components for use with Meresco
#
# Copyright (C) 2008-2010 Seek You Too (CQ2) http://www.cq2.nl
# Copyright (C) 2008-2009 Technische Universiteit Delft http://www.tudelft.nl
# Copyright (C) 2008-2009 Universiteit van Tilburg http://www.uvt.nl
# Copyright (C) 2019 Seecr (Seek You Too B.V.) https://seecr.nl
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

from StringIO import StringIO

from unittest import TestCase

from meresco.normalize.name.namenormalize import lastnameAndInitials, lastnameAndFirstInitial, lastname, unparsable, firstLetter, _breakUp, _helsing_v, _helsing_a_v, _helsing_ab_van, givenname, familyname, _BreakUpResult

def helsing_v((lastname, initials, prefix)):
    return _helsing_v(_BreakUpResult(lastname, '', initials, prefix))
def helsing_a_v((lastname, initials, prefix)):
    return _helsing_a_v(_BreakUpResult(lastname, '', initials, prefix))
def helsing_ab_van((lastname, initials, prefix)):
    return _helsing_ab_van(_BreakUpResult(lastname, '', initials, prefix))

class NameNormalizeTest(TestCase):

    def assertLastnameAndInitials(self, expected, input=""):
        if not input:
            input = expected
        self.assertEquals(expected, lastnameAndInitials(input).next())

    def testLastnameAndInitials(self):
        self.assertLastnameAndInitials("Peters, H.")
        self.assertLastnameAndInitials("Peters, H.J.M.")
        self.assertLastnameAndInitials("Peters, H.J.M.", "Peters, H. J. M.")
        self.assertLastnameAndInitials("Guillen Scholten, J.V.", "Guillen Scholten, J. V.")
        self.assertLastnameAndInitials("Peters, H.", "Peters, Hans")
        self.assertLastnameAndInitials("Peters, H.", "Peters, H")
        self.assertLastnameAndInitials("Peters, H.", "Peters, H. (Hans)")
        self.assertLastnameAndInitials("Peters, H.J.M.", "Peters, H.J.M. (Hans)")
        self.assertLastnameAndInitials("Peters, H.", "Peters, H. (Hans Jan Marie)")
        self.assertLastnameAndInitials("Peters, H.J.M.", "Peters, HJM")
        self.assertLastnameAndInitials("Peters, H.J.M.", "Peters, Hans Jan Marie")
        self.assertLastnameAndInitials("Peters, J.J.", "Peters, J.-J.")
        self.assertLastnameAndInitials("Peters, J.J.", "Peters, J-J.")
        self.assertLastnameAndInitials("Somers, V.A.M.C.", "Somers, Veerle Anne-Marie Christine")
        self.assertLastnameAndInitials("Vissers, F.H.J.A.", "Vissers, Frans H.J.A.")
        self.assertLastnameAndInitials("Berg, G.J. van den", "Berg, G. J. van den")
        self.assertLastnameAndInitials("Berg, G.J. van den", "Berg, Gerard J. van den")
        self.assertLastnameAndInitials("Franses, Ph.H.B.F.")
        self.assertLastnameAndInitials("Heiden, A.F.Th. van der")
        self.assertLastnameAndInitials("Lämmel, R.")
        self.assertLastnameAndInitials("Ämmel, R.")
        self.assertLastnameAndInitials("Ba'ath, R.")
        self.assertLastnameAndInitials("IJssel, R.")
        self.assertLastnameAndInitials("Lämmel, É.")
        self.assertLastnameAndInitials("Lämmel, É.", "Lämmel, Érik")
        self.assertLastnameAndInitials("Lämmel, É.", "Lämmel, É. (Érik)")
        self.assertLastnameAndInitials('Núñez-Queija, R.')
        self.assertLastnameAndInitials("Eind, A. 't")
        self.assertLastnameAndInitials("Peters, H. van")
        self.assertLastnameAndInitials("Peters, H. van der")
        self.assertLastnameAndInitials("Peters, H.J.M. van")
        self.assertLastnameAndInitials("Peters, H.J.M. van", "Peters, H. J. M. van")
        self.assertLastnameAndInitials("Bart, P.A.", "Bart, P.-A. (Pierre-Alexandre)")
        #self.assertLastnameAndInitials("Groeneveld, E.J.", "Erik J.Groeneveld")
        #self.assertLastnameAndInitials("Bunch, T.J.", "Bunch.T.Jared")
        #self.assertLastnameAndInitials("Bunch, T.J.", "B T.Bunch")
        #self.assertLastnameAndInitials("Bunch, T.J.", "B.T.Bunch")
        #self.assertLastnameAndInitials("Jared-Morehouse, B.T.", "Bunch T.Jared-Morehouse")
        self.assertLastnameAndInitials("Ba'ath, B.T.", "Bunch T.Ba'ath")
        self.assertLastnameAndInitials("Groeneveld, E.J.", "E.J. Groeneveld (Lord)")
        self.assertLastnameAndInitials("Groeneveld, E.", "E. (Groeneveld)")
        self.assertLastnameAndInitials("Groeneveld", "Groeneveld")
        self.assertLastnameAndInitials("Groeneveld", "(Groeneveld)")
        self.assertLastnameAndInitials("Groeneveld-Dijkema", "(Groeneveld-Dijkema)")
        self.assertLastnameAndInitials("Groen'veld", "(Groen'veld)")
        self.assertLastnameAndInitials("Groen'veld-Dijkema", "(Groen'veld-Dijkema?)")
        self.assertLastnameAndInitials("Açıkel, Y.S.", "Açıkel, Y. Sağ")

    def testOrganisationNames(self):
        self.assertLastnameAndInitials("Universiteit van Amsterdam", "Universiteit van Amsterdam")
        self.assertLastnameAndInitials("Voeikov Main Geophysical Observatory", "A.I. Voeikov Main Geophysical Observatory")
        self.assertLastnameAndInitials("Zhdanov State University", "A.A. Zhdanov State University, Leningrad")
        self.assertLastnameAndInitials('Association for Computing Machinery', "Association for Computing Machinery")
        self.assertLastnameAndInitials('Institute of Electrical and Electronics Engineers', "Institute of Electrical and Electronics Engineers, Inc.")
        self.assertLastnameAndInitials("Kearney and Company", "A.T. Kearney and Company")
        self.assertLastnameAndInitials("Committee on Entrainment", "AD Hoc Committee on Entrainment")
        self.assertLastnameAndInitials("Agard Propulsion and Energetics Panel Meeting", "AGARD Propulsion and Energetics Panel Meeting")
        self.assertLastnameAndInitials("Akademija Nauk Sssr", "AKADEMIJA Nauk SSSR, Institut Mashinovedenija")
        self.assertLastnameAndInitials("Asee-Nasa Langley Research Center", "ASEE-NASA Langley Research Center")
        self.assertLastnameAndInitials("Aartsbisschoppelijk Museum Utrecht", "Aartsbisschoppelijk Museum Utrecht")
        self.assertLastnameAndInitials("Abbotsford International Airshow Society", "Abbotsford International Airshow Society")
        self.assertLastnameAndInitials("Aerofilm and Aero Pictorial Limited", "Aerofilm and Aero Pictorial Limited, Library")
        self.assertLastnameAndInitials("Aerospace Division", "Aerospace Division, Structures and Materials Committee")
        self.assertLastnameAndInitials("Air Force Systems Command", "Air Force Systems Command, Foreign Technology Division")
        self.assertLastnameAndInitials("Algemeen Pedagogisch Studiecentrum", "Algemeen Pedagogisch Studiecentrum, Afdeling Wetenschappelijk Bureau")
        self.assertLastnameAndInitials("Algemene Verladers- En Eigen Vervoerdersorganisatie", "Algemene Verladers- en Eigen Vervoerdersorganisatie, Afdeling Intern Transport- en Opslag")
        self.assertLastnameAndInitials("Allgemeine Mikrobiologie und Verfahrensgrundlagen Zur Erhaltung von Lebensmitteln", "Allgemeine Mikrobiologie und Verfahrensgrundlagen zur Erhaltung von Lebensmitteln, Deutsland")
        self.assertLastnameAndInitials("Party for International Business", "Party for International Business, Amsterdam")
        self.assertLastnameAndInitials("Partij voor de Dieren", "Partij voor de Dieren, Nederland")
        self.assertLastnameAndInitials("Ifip Congress on Information Processing", "1962 IFIP Congress on Information Processing")
        self.assertLastnameAndInitials("Ifip Congress on Information Processing", "1962 IFIP Congress on Information Processing; Munich, Aug./Sept. 1962")
        #self.assertLastnameAndInitials("", "AIAA Conference on Air Transportation: Technical perspectives and forecasts; Los Angeles, Aug. 1978")
        #self.assertLastnameAndInitials("", "AIAA Guidance, Control and Flight Mechanics Conference; Santa Barbara, Aug. 1970")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")
        #self.assertLastnameAndInitials("", "")

    def testBug(self):
        pass
        #from re import compile

        #regexp = compile(r"^(\w+\s*){0,6}$")
        #s = 'eenentwintig twee drie vier vijf zes.'
        #result = regexp.match(s)

        #print "stap 1"


        #regexp = compile(r'^(?P<lastname>[\w\-\s]+)[,\.] (?P<initials>(\w{1,2}[\.\s])+)\s*' + r"(?P<prefix>(?:(?:\w+|'t)\s*)*)$")
        #s = 'De Groot R, ab eenentwintig tweeentwintig drie vier vijf zes.'
        #result = regexp.match(s)

        #print result

        #regexp = compile(r'^(?P<lastname>[\w\-\s]+)[,\.] (?P<initials>(\w{1,2}[\.\s])+)\s*' + r"(?P<prefix>(?:(?:\w+|'t)\s*)*)$")
        #s = 'De Groot R, on behalf of the Dutch study group for children with, HI.V.-1 infections.'
        #regexp.match(s)


    def assertLastnameAndFirstInitial(self, expected, input=""):
        if not input:
            input = expected
        self.assertEquals(expected, lastnameAndFirstInitial(input).next())

    def assertUnparsable(self, name):
        self.assertEquals(name, unparsable(name).next())

    def testNotYetNormalized(self):
        self.assertUnparsable('This$Will$@*NotBeAName')
        self.assertUnparsable('(Captain)')
        self.assertUnparsable('(captain)')
        self.assertUnparsable('(Baron)')
        self.assertUnparsable('(Countess)')
        self.assertUnparsable('(Cid)')
        self.assertUnparsable('(Earl)')
        self.assertUnparsable('(Fellow)')
        self.assertUnparsable('(Fils)')
        self.assertUnparsable('(Frhr)')
        self.assertUnparsable('(Freiherr)')
        self.assertUnparsable('(Graaf)')
        self.assertUnparsable('(Graf)')
        self.assertUnparsable('(Jeune)')
        self.assertUnparsable('(Jr)')
        self.assertUnparsable('(Lady)')
        self.assertUnparsable('(Lord)')
        self.assertUnparsable('(Meenenaer)')
        self.assertUnparsable('(Prins)')
        self.assertUnparsable('(Prinses)')
        self.assertUnparsable('(Ritter)')
        self.assertUnparsable('(Sir)')
        self.assertUnparsable('(Wzn)')
        self.assertUnparsable('(Daventriensis)')
        self.assertUnparsable('11th, Munich')
        self.assertUnparsable('14th')
        self.assertUnparsable('1966')
        self.assertUnparsable('1st Division')
        self.assertUnparsable('2e Division')
        self.assertUnparsable('I')
        self.assertUnparsable('III')
        self.assertUnparsable('IV')
        self.assertUnparsable('(XI)')

    def testLastnameAndFirstInitial(self):
        self.assertLastnameAndFirstInitial("Peters, H.")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, H.J.M.")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, H. J. M.")
        self.assertLastnameAndFirstInitial("Guillen Scholten, J.", "Guillen Scholten, J. V.")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, Hans")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, H")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, H. (Hans)")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, H.J.M. (Hans)")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, H. (Hans Jan Marie)")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, HJM")
        self.assertLastnameAndFirstInitial("Peters, H.", "Peters, Hans Jan Marie")
        self.assertLastnameAndFirstInitial("Peters, J.", "Peters, J.-J.")
        self.assertLastnameAndFirstInitial("Peters, J.", "Peters, J-J.")
        self.assertLastnameAndFirstInitial("Somers, V.", "Somers, Veerle Anne-Marie Christine")
        self.assertLastnameAndFirstInitial("Vissers, F.", "Vissers, Frans H.J.A.")
        self.assertLastnameAndFirstInitial("Berg, G. v.d.", "Berg, G. J. van den")
        self.assertLastnameAndFirstInitial("Berg, G. v.d.", "Berg, Gerard J. van den")
        self.assertLastnameAndFirstInitial("Franses, Ph.", "Franses, Ph.H.B.F.")
        self.assertLastnameAndFirstInitial("Heiden, A. v.d.", "Heiden, A.F.Th. van der")
        self.assertLastnameAndFirstInitial("Lämmel, R.")
        self.assertLastnameAndFirstInitial("Ämmel, R.")
        self.assertLastnameAndFirstInitial("Lämmel, É.")
        self.assertLastnameAndFirstInitial("Lämmel, É.", "Lämmel, Érik")
        self.assertLastnameAndFirstInitial("Lämmel, É.", "Lämmel, É. (Érik)")
        self.assertLastnameAndFirstInitial('Núñez-Queija, R.')
        self.assertLastnameAndFirstInitial("Eind, A. 't")
        self.assertLastnameAndFirstInitial("Peters, H. v.","Peters, H. van")
        self.assertLastnameAndFirstInitial("Peters, H. v.d.", "Peters, H. van der")
        self.assertLastnameAndFirstInitial("Peters, H. v.", "Peters, H.J.M. van")
        self.assertLastnameAndFirstInitial("Peters, H. v.", "Peters, H. J. M. van")
        self.assertLastnameAndFirstInitial("Beaumont, W.", "Beaumont, W.Worby")
        self.assertLastnameAndFirstInitial("Petri, N.", "Petri, Nicolaus (Daventriensis)")
        self.assertLastnameAndFirstInitial("Açıkel, Y.", "Açıkel, Y. Sağ")

    def assertLastname(self, expected, input=""):
        if not input:
            input = expected
        self.assertEquals(expected, lastname(input).next())

    def testLastname(self):
        self.assertLastname("Peters", "Peters, H.")
        self.assertLastname("Peters", "Peters, H.J.M.")
        self.assertLastname("Peters", "Peters, H. J. M.")
        self.assertLastname("Guillen Scholten", "Guillen Scholten, J. V.")
        self.assertLastname("Peters", "Peters, Hans")
        self.assertLastname("Peters", "Peters, H")
        self.assertLastname("Peters", "Peters, H. (Hans)")
        self.assertLastname("Peters", "Peters, H.J.M. (Hans)")
        self.assertLastname("Peters", "Peters, H. (Hans Jan Marie)")
        self.assertLastname("Peters", "Peters, HJM")
        self.assertLastname("Peters", "Peters, Hans Jan Marie")
        self.assertLastname("Peters", "Peters, J.-J.")
        self.assertLastname("Peters", "Peters, J-J.")
        self.assertLastname("Somers", "Somers, Veerle Anne-Marie Christine")
        self.assertLastname("Vissers", "Vissers, Frans H.J.A.")
        self.assertLastname("Berg, v.d.", "Berg, G. J. van den")
        self.assertLastname("Berg, v.d.", "Berg, Gerard J. van den")
        self.assertLastname("Franses", "Franses, Ph.H.B.F.")
        self.assertLastname("Heiden, v.d.", "Heiden, A.F.Th. van der")
        self.assertLastname("Lämmel", "Lämmel, R.")
        self.assertLastname("Ämmel", "Ämmel, R.")
        self.assertLastname("Lämmel", "Lämmel, É.")
        self.assertLastname("Lämmel", "Lämmel, Érik")
        self.assertLastname("Lämmel", "Lämmel, É. (Érik)")
        self.assertLastname('Núñez-Queija', 'Núñez-Queija, R.')
        self.assertLastname("Eind, 't", "Eind, A. 't")
        self.assertLastname("Peters, v.","Peters, H. van")
        self.assertLastname("Peters, v.d.", "Peters, H. van der")
        self.assertLastname("Peters, v.", "Peters, H.J.M. van")
        self.assertLastname("Peters, v.", "Peters, H. J. M. van")
        self.assertLastname("Açıkel", "Açıkel, Y. Sağ")


    def test_breakUp(self):
        self.assertEquals(None, _breakUp(""))
        self.assertEquals([str, str, str, str], [type(e) for e in _breakUp("Peters, H.")])
        self.assertEquals(("peters", "h.", "h.", ""), _breakUp("Peters, H."))
        self.assertEquals(("peters", "h.j.m.", "h.j.m.", ""), _breakUp("Peters, H.J.M."))
        self.assertEquals(("peters", "h. j. m.", "h.j.m.", ""), _breakUp("Peters, H. J. M."))
        self.assertEquals(("guillen scholten", "j. v.", "j.v.", ""), _breakUp("Guillen Scholten, J. V."))

    def test_breakUpInitials(self):
        self.assertEquals(("peters", "hans", "h.", ""), _breakUp("Peters, Hans"))
        self.assertEquals(("peters", "h", "h.", ""), _breakUp("Peters, H"))
        self.assertEquals(("peters", "h.", "h.", ""), _breakUp("Peters, H. (Hans)"))
        self.assertEquals(("peters", "h.", "h.", ""), _breakUp("Peters, H. (ed.)"))
        self.assertEquals(("peters", "h.", "h.", ""), _breakUp("Peters. H."))
        self.assertEquals(("peters", "h.j.m.", "h.j.m.", ""), _breakUp("Peters, H.J.M. (Hans)"))
        self.assertEquals(("peters", "h.", "h.", ""), _breakUp("Peters, H. (Hans Jan Marie)"))
        self.assertEquals(("peters", "hjm", "h.j.m.", ""), _breakUp("Peters, HJM"))
        self.assertEquals(("peters", "hans jan marie", "h.j.m.", ""), _breakUp("Peters, Hans Jan Marie"))
        self.assertEquals(("peters", "j.-j.", "j.j.", ""), _breakUp("Peters, J.-J."))

        self.assertEquals(("peters", "j-j.", "j.j.", ""), _breakUp("Peters, J-J."))
        self.assertEquals(("somers","veerle anne-marie christine","v.a.m.c.",""), _breakUp("Somers, Veerle Anne-Marie Christine"))
        self.assertEquals(("vissers","frans h.j.a.","f.h.j.a.",""), _breakUp("Vissers, Frans H.J.A."))
        self.assertEquals(("berg","g. j.","g.j.","van den"), _breakUp("Berg, G. J. van den"))
        self.assertEquals(("berg","gerard j.","g.j.","van den"), _breakUp("Berg, Gerard J. van den"))
        self.assertEquals(("berg","a.p.","a.p.","van den"), _breakUp("Berg, A.P. (Arie) van den"))
        self.assertEquals(("franses","ph.h.b.f.","ph.h.b.f.",""), _breakUp("Franses, Ph.H.B.F.")) #??
        self.assertEquals(("heiden","a.f.th.","a.f.th.","van der"), _breakUp("Heiden, A.F.Th. van der")) #??
        self.assertEquals(("peters", "hans", "h.", ""), _breakUp("Peters, Hans"))
        self.assertEquals(("beaumont", "w.worby", "w.w.", ""), _breakUp("Beaumont, W.Worby"))
        self.assertEquals(("petri", "nicolaus", "n.", ""), _breakUp("Petri, Nicolaus (Daventriensis)"))

    def test_breakUpUtf8(self):
        self.assertEquals(("lämmel", "r.", "r.", ""), _breakUp("Lämmel, R."))
        self.assertEquals(("ämmel", "r.", "r.", ""), _breakUp("Ämmel, R."))
        self.assertEquals(("lämmel", "é.", "é.", ""), _breakUp("Lämmel, É."))
        self.assertEquals(("lämmel", "érik", "é.", ""), _breakUp("Lämmel, Érik"))
        self.assertEquals(("lämmel", "é.", "é.", ""), _breakUp("Lämmel, É. (Érik)"))
        self.assertEquals(("núñez-queija", "r.", "r.", ""), _breakUp('Núñez-Queija, R.'))
        self.assertEquals(("açıkel","y. sağ","y.s.", ""), _breakUp("Açıkel, Y. Sağ"))

    def test_breakUpPrefix(self):
        self.assertEquals(("eind", "a.", "a.", "'t"), _breakUp("Eind, A. 't"))
        self.assertEquals(("peters", "h.", "h.", "van"), _breakUp("Peters, H. van"))
        self.assertEquals(("peters", "h.", "h.", "van der"), _breakUp("Peters, H. van der"))
        self.assertEquals(("peters", "h.j.m.", "h.j.m.", "van"), _breakUp("Peters, H.J.M. van"))
        self.assertEquals(("peters", "h. j. m.", "h.j.m.", "van"), _breakUp("Peters, H. J. M. van"))

        #self.assertEquals(("peters", "h", "v"), _breakUp("Peters, H. v.")) #?
        #naam: achter tussen voor initialen titels
        #self.assertEquals(("peters", "", "j", ["j", "j"]), _breakUp("Peters, Jean-Jacques"))

    def testCompose(self):
        self.assertEquals("Helsing", helsing_v(("helsing", "a.b.", "")))
        self.assertEquals("Helsing, v.", helsing_v(("helsing", "a.b.", "van")))
        self.assertEquals("Helsing, A.", helsing_a_v(("helsing", "a.b.", "")))
        self.assertEquals("Helsing, A. v.", helsing_a_v(("helsing", "a.b.", "van")))
        self.assertEquals("Helsing, A. v.d.", helsing_a_v(("helsing", "a.b.", "van der")))
        self.assertEquals("Helsing, A.B.", helsing_ab_van(("helsing", "a.b.", "")))
        self.assertEquals("Helsing, A.B. van", helsing_ab_van(("helsing", "a.b.", "van")))
        self.assertEquals("Helsing, A.B. van der", helsing_ab_van(("helsing", "a.b.", "van der")))
        self.assertEquals("IJmuiden", helsing_v(("ijmuiden", "t.", "")))
        self.assertEquals("Israël", helsing_v(("israël", "t.", "")))

    def testFirstLetter(self):
        self.assertEquals(int('f1', 16), ord(u'ñ'))
        self.assertEquals(u'ñ', unicode('ñ'))
        self.assertEquals('\xc3\xb1', u'ñ'.encode('utf-8'))
        self.assertEquals('\xc3\xb1', str(u'ñ'))
        self.assertEquals(['A'], list(firstLetter("Alberts, J.")))
        self.assertEquals([str('Ñ')], list(firstLetter("ñiño, el")))

    def testNamesInOtherFormat(self):
        self.assertEquals(('groeneveld', 'e.', 'e.', ''), _breakUp('E. Groeneveld'))
        self.assertEquals(('groeneveld', 'e. g.', 'e.g.', ''), _breakUp('E. G. Groeneveld'))
        self.assertEquals(('groeneveld', 'é. û.', 'é.û.', ''), _breakUp('É. Û. Groeneveld'))
        brokenUp = _breakUp('H. G. Ruhé')
        self.assertEquals(('ruhé', 'h. g.', 'h.g.', ''), brokenUp)
        result = _helsing_a_v(brokenUp)
        self.assertEquals('Ruhé, H.', result)

    def testFurtherImprovementsFromTUDtestData(self):
        self.assertLastnameAndInitials("Ahan", "ahan")
        self.assertLastname("Ahan", "ahan")
        self.assertLastnameAndInitials("'s Gravesande Guicherit, M.A.M.", "'s Gravesande Guicherit, M.A.M.")
        self.assertLastname("'s Gravesande Guicherit", "'s Gravesande Guicherit, M.A.M.")
        #self.assertLastnameAndInitials("?", "'s Gravesande, Willem Jacob.")
        #self.assertLastnameAndInitials("?", "'s-Gravesande, Guillaume Jacob.")
        #self.assertLastnameAndInitials("?", "Antonio Gustavo S.")
        self.assertLastnameAndInitials("Het Oversticht", "'Het Oversticht', Genootschap tot Bevordering en Instandhouding van het Landelijk en Stedelijk Schoon in de Provincie Overijssel")
        #self.assertLastnameAndInitials('Adeline', "Adeline A.")
        #self.assertLastnameAndInitials('Agricola, G.', "Agricola, Georgius.")
        #self.assertLastnameAndInitials('?', "Ahiaku, geb. Brew, Comfort Akyima")
        #self.assertLastnameAndInitials('Ahlburg, J.', "Ahlburg, Joh.")

    def testFamilynameGivenname(self):
        def assertFamilynameGivenname(expected_familyname, expected_givenname, name):
            familyresult = first(familyname(name))
            givenresult = first(givenname(name))
            self.assertEqual((expected_familyname, expected_givenname), (familyresult, givenresult))
        assertFamilynameGivenname('Peters', 'H.', "Peters, H.")
        # ("Peters, H.J.M.")
        # ("Peters, H.J.M.", "Peters, H. J. M.")
        # ("Guillen Scholten, J.V.", "Guillen Scholten, J. V.")
        # ("Peters, H.", "Peters, Hans")
        # ("Peters, H.", "Peters, H")
        # ("Peters, H.", "Peters, H. (Hans)")
        # ("Peters, H.J.M.", "Peters, H.J.M. (Hans)")
        # ("Peters, H.", "Peters, H. (Hans Jan Marie)")
        # ("Peters, H.J.M.", "Peters, HJM")
        # ("Peters, H.J.M.", "Peters, Hans Jan Marie")
        # ("Peters, J.J.", "Peters, J.-J.")
        # ("Peters, J.J.", "Peters, J-J.")
        # ("Somers, V.A.M.C.", "Somers, Veerle Anne-Marie Christine")
        # ("Vissers, F.H.J.A.", "Vissers, Frans H.J.A.")
        # ("Berg, G.J. van den", "Berg, G. J. van den")
        # ("Berg, G.J. van den", "Berg, Gerard J. van den")
        # ("Franses, Ph.H.B.F.")
        # ("Heiden, A.F.Th. van der")
        # ("Lämmel, R.")
        # ("Ämmel, R.")
        # ("Ba'ath, R.")
        # ("IJssel, R.")
        # ("Lämmel, É.")
        # ("Lämmel, É.", "Lämmel, Érik")
        # ("Lämmel, É.", "Lämmel, É. (Érik)")
        # ('Núñez-Queija, R.')
        # ("Eind, A. 't")
        # ("Peters, H. van")
        # ("Peters, H. van der")
        # ("Peters, H.J.M. van")
        # ("Peters, H.J.M. van", "Peters, H. J. M. van")
        # ("Bart, P.A.", "Bart, P.-A. (Pierre-Alexandre)")
        #self.assertLastnameAndInitials("Groeneveld, E.J.", "Erik J.Groeneveld")
        #self.assertLastnameAndInitials("Bunch, T.J.", "Bunch.T.Jared")
        #self.assertLastnameAndInitials("Bunch, T.J.", "B T.Bunch")
        #self.assertLastnameAndInitials("Bunch, T.J.", "B.T.Bunch")
        #self.assertLastnameAndInitials("Jared-Morehouse, B.T.", "Bunch T.Jared-Morehouse")
        # ("Ba'ath, B.T.", "Bunch T.Ba'ath")
        # ("Groeneveld, E.J.", "E.J. Groeneveld (Lord)")
        # ("Groeneveld, E.", "E. (Groeneveld)")
        # ("Groeneveld", "Groeneveld")
        # ("Groeneveld", "(Groeneveld)")
        # ("Groeneveld-Dijkema", "(Groeneveld-Dijkema)")
        # ("Groen'veld", "(Groen'veld)")
        # ("Groen'veld-Dijkema", "(Groen'veld-Dijkema?)")
        # ("Açıkel, Y.S.", "Açıkel, Y. Sağ")


def first(it, default=None):
    try:
        return it.next()
    except StopIteration:
        return default


