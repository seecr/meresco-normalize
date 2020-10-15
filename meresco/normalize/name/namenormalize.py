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
from re import compile, UNICODE, IGNORECASE

def lower(initials):
    return initials.lower()

wordSplitter = compile(r'(?<=\w)\w*[ \-\.]*', UNICODE)

def getInitials(firstNames):
    return [aChar.lower() for aChar in wordSplitter.split(firstNames) if aChar]

def addDots(initiialList):
    return ".".join(initiialList) + "."

def getDoubleInitials(firstNames):
    return [initial.lower() for initial in firstNames.split('.') if initial]

# e.g. "Johnson"
lastname = r"\(?(?P<lastname>[\w\-'\s]+)\)?"
# e.g. "", "de", "van de", "van 't"
prefix = r"(?P<prefix>|(?:van|de|der|den|'t)(?:\s+(?:van|de|der|den|'t)){0,2})"
punctuation = r'(, |\. |,|\.)'
comment= r'(?:|\([\w\s\.\-]+\))\s*'

expressions = [
    # e.g. "M.P.D."  (WhaAAtevaesdf)
    (r'(?P<initials>(\w\. )+)'+lastname, getInitials),
    # e.g. "Johnson-Peter'son, M. P-  D (Some-Extra stuff.) van den"
    ('^'+lastname+punctuation+r'(?P<initials>(?:\w[\.\-]{1,2}\s*)+)\s*'+comment+prefix+'$',getInitials),
    # e.g. "Johnson, MPD"
    ('^'+lastname+punctuation+r'(?P<initials>[A-Z]+)$', lower),
    # e.g. "Johnson, M P-D"
    ('^'+lastname+punctuation+r'(?P<initials>[\w\s\-]+)$', getInitials),
    # e.g. "Johnson, Pete  D.L.  "
    ('^'+lastname+punctuation+r'(?P<initials>\w+\s+(\w\.)+)\s*'+prefix+'$',getInitials),
    # e.g. "Johnson, L. Pete"
    ('^'+lastname+punctuation+r'(?P<initials>(\w\.)+\s+\w+)\s*'+'$',getInitials),
    # e.g. "Johnson,  M. Ph  D."
    ('^'+lastname+punctuation+r'(?P<initials>(\w{1,2}[\.\s])+)\s*'+prefix+'$', getDoubleInitials),
    # e.g. "Johnson, P.Desiree"
    ('^'+lastname+punctuation+r'(?P<initials>(\w\.\w+))$', getInitials),
    # e.g. "Johnson, John-Peter George (Lord-of-the-Rings)"
    ('^'+lastname+punctuation+r'(?P<initials>[\w\s\-]+)'+r'\s*(?:\([\w\s\.\-]+\))\s*', getInitials),
    # e.g. "Maria P.Johnson", "Maria.P.Johnson."
    (r'^(?P<initials>\w+[ \.]\w\.)'+lastname, getInitials),
    # e.g. "Maria J."

    # e.g. "(Johnson)", "Johnson-Peter'son?"
    (r'^\(?(?P<lastname>[\w\-\']+)\??\)?$', None),
    # e.g. "Association for Computing Machinery, Inc."
    (r'^(?P<lastname>[\w\-]+(\s[\w\-]+)*)((, )(Inc|Inc\.|Incorporated))?$', None),
    # "Adeline A."
    #(r"(?P<lastname>\w+)\s\w\.", None),
    # "Agricola, Georgius."
    #(r"(?P<lastname>\w+),\s(?P<initials>\w)\w*?\.", getInitials),
]

specificExpressions = [
    # (Lord), (Lady), etc
    (IGNORECASE, r'\(Captain\)|\(Baron\)|\(Countess\)|\(Cid\)|\(Earl\)|\(Fellow\)|\(Fils\)|\(Frhr\)|\(Freiherr\)|\(Graaf\)|\(Graf\)|\(Grossherzog\)|\(Jeune\)|\(Jr\)|\(Lady\)|\(Lord\)|\(Meenenaer\)|\(Prins\)|\(Prinses\)|\(Ritter\)|\(Sir\)|\(Wzn\)|\(Daventriensis\)|\(\)|\(\)|\(\)|\(\)|\(\)'),
    # "Roman numbers optionally in ( ), "XVI", "(MXXII)"
    (0, r'^\(?[IVXMCL]+\)?$'),
    # "1e Divisie", "1998", "1997, Munich" etc
    (IGNORECASE, r'^\d+(th|nd|st|e)?,?\s?(\w+)?$'),
    # Academy, University, Sciene etc
    (IGNORECASE, r'(ad\shoc)?[\w\.]*?(\d\d\d\d)?\s?(?P<result>[\w\s\-]*?(a[ck]adem|science|abteilung|society|museum|school|universit|college|foundation|corporation|company|ass?ocia[tcz]ion|organi[sz]ati|observatory|committee|limited|ltd|division|afdeling|research|laborator|centre|center|centrum|command|all?gemei?ne|international|maatschappij|bibliothe|library|departe?ment|group|service|[ck]ommissi|part(y|ij)|stichting|panel|project|council|gemeinschaft|arbeitsgruppe|werkgroep|arbeitskreis|gemeenschap|verein|forschung|institut|experiment|hospital|agency|assembly|atelier|forum|board|gmbh|fabrie?k|congres)[\w\s\-]*)'),
    # "'Het Gesticht', Een instelling voor programmeurs."
    (0, r"\'(?P<result>[\w\s]+)\',[\s\w]+"),
]

compiledExpressions = [(compile(expression, UNICODE),f) for expression,f in expressions]
compiledSpecificExpressions = [compile(expression, flags|UNICODE) for flags, expression in specificExpressions]

def _breakUp(name):
    if type(name) != str:
        name = str(name)
    for expression in compiledSpecificExpressions:
        m = expression.match(name)
        if m:
            if 'result' in m.groupdict():
                return m.groupdict()['result'].lower(), '', ''
            else:
                return None
    for expression, initialsPostProcess in compiledExpressions:
        m = expression.match(name)
        if m:
            lastname = m.groupdict()['lastname'].lower()
            lastname = lastname.strip()
            if initialsPostProcess:
                initials = addDots(initialsPostProcess(m.groupdict()['initials']))
            else:
                initials = ''
            prefix = m.groupdict().get('prefix', "")
            return str(lastname), str(initials), str(prefix)
    return None


def dots(s):
    return "".join([c + "." for c in s])

def _firstChar(s):
    return s and s[0]

_capitalizeRegexp = compile(r"(ij|'s|\w)([\w']*)", UNICODE)
def _capitalizeSubstite(match):
    firstLetter = match.group(1)
    tail = match.group(2)
    word = firstLetter+tail
    if word in ['van', 'der','voor',  'for', 'and', 'of', 'from', 'on', 'the', 'an', 'as', "'s", 'und', 'von', 'de', 'des', 'les', 'du', 'dei', 'di']:
        return word
    return firstLetter.upper() + tail

def _capitalize(aString):
    return str(_capitalizeRegexp.sub(_capitalizeSubstite, str(aString)))

def _helsing_v(lastname, initials, prefix):
    prefix = ''.join([aChar == "'t" and aChar or aChar+"." for aChar in getInitials(prefix)])
    result = _capitalize(lastname)
    if prefix:
        return result + ", " + prefix
    return result

def _helsing_a_v(lastname, initials, prefix):
    prefix = ''.join([aChar == "'t" and aChar or aChar+"." for aChar in getInitials(prefix)])
    initials = initials.split('.', 1)[0] + '.'
    result = "%s, %s" % (_capitalize(lastname), _capitalize(initials))
    if prefix:
        return result + " " + prefix
    return result

def _helsing_ab_van(lastname, initials, prefix):
    if initials:
        result = "%s, %s" % (_capitalize(lastname), _capitalize(initials))
    else:
        result = _capitalize(lastname)
    if prefix:
        return result + " " + prefix
    return result

def lastname(unparsedName):
    parts = _breakUp(unparsedName)
    if parts:
        yield _helsing_v(*parts)

def lastnameAndFirstInitial(unparsedName):
    parts = _breakUp(unparsedName)
    if parts:
        yield _helsing_a_v(*parts)

def lastnameAndInitials(unparsedName):
    parts = _breakUp(unparsedName)
    if parts:
        yield _helsing_ab_van(*parts)

def firstLetter(unparsedName):
    parts = _breakUp(unparsedName)
    if parts:
        lastname, initials, prefix = parts
        lastname = str(lastname)
        yield str(lastname[:1].upper())

def unparsable(unparsedName):
    parts = _breakUp(unparsedName)
    if not parts:
        yield unparsedName
