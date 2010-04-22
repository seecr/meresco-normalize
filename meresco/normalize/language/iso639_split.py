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

if __name__ == '__main__':
    # NL source: http://nl.wikipedia.org/wiki/Lijst_van_ISO_639-1-codes (copy/paste from page source in edit screen)
    sourceNl = open('iso639-2_nl.txt').read()
    lines=sourceNl.split('|----\n')

    results = {}
    for line in lines:
        parts = line[1:].split('||')
        if len(parts) > 3 and not parts[1].startswith('--'):
            languageCode2 = parts[0]
            languageCode3 = parts[1]
            languageName = parts[3].replace('[', '').replace(']', '')
            if '|' in languageName:
                languageName = languageName.split('|')[-1]
            if ',' in languageName:
                languageName = languageName.split(',')[0]
            if '/' in languageCode3:
                languageCode3 = languageCode3.split('/')[0]
            if '/' in languageCode2:
                languageCode2 = languageCode2.split('/')[0].strip()

            results[languageCode3] = (languageCode2, {'nl': languageName})


    # EN source: http://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt
    sourceEn = open('ISO-639-2_utf-8.txt').read()
    lines=sourceEn.split('\n')

    for line in lines:
        parts =  line.split('|')

        languageCode3 = parts[0]
        languageName = parts[3]

        if ';' in languageName:
            languageName = languageName.split(';')[0]
        if ',' in languageName:
            languageName = languageName.split(',')[0]

        if languageCode3 in results:
            languageCode2, nameDictionary = results[languageCode3]
            nameDictionary['en'] = languageName
            results[languageCode3] = (languageCode2, nameDictionary)


    fp = open('iso639-2_nl_en.txt', 'w')
    try:
        for languageCode in sorted(results):
            languageCode2, nameDictionary = results[languageCode]
            if len(nameDictionary) != 2:
                print languageCode, languageCode2, nameDictionary
            fp.write("%s\t%s\t%s\t%s\n" % (languageCode, languageCode2, nameDictionary['nl'], nameDictionary['en']))
    finally:
        fp.close()
