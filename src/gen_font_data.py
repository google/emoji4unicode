#!/usr/bin/python2.4
#
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generate data for the proposal font database."""

__author__ = "Markus Scherer"

import codecs
import os.path
import sys
import emoji4unicode
import utf

POST_HEADER = u"""<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<!DOCTYPE postTable [
<!ELEMENT postTable (PostScriptName+)>
<!ELEMENT PostScriptName EMPTY>
<!ATTLIST postTable versionMajor CDATA #REQUIRED
    versionMinor CDATA #REQUIRED
    italicAngle CDATA #REQUIRED
    underlinePosition CDATA #REQUIRED
    underlineThickness CDATA #REQUIRED
    isFixedPitch CDATA #REQUIRED
    minMemType42 CDATA #REQUIRED
    maxMemType42 CDATA #REQUIRED
    minMemType1 CDATA #REQUIRED
    maxMemType1 CDATA #REQUIRED>
<!ATTLIST PostScriptName glyphRefID CDATA #REQUIRED
    PostScriptIndex CDATA #IMPLIED
    NameString CDATA #REQUIRED>
]>

<postTable  versionMajor="2"
    versionMinor="0"
    italicAngle="0.0"
    underlinePosition="-85"
    underlineThickness="155"
    isFixedPitch="0"
    minMemType42="0"
    maxMemType42="0"
    minMemType1="0"
    maxMemType1="0">
  <PostScriptName glyphRefID="0" NameString=".notdef" />
  <PostScriptName glyphRefID="1" NameString="uni0000" />
  <PostScriptName glyphRefID="2" NameString="nonmarkingreturn" />
  <PostScriptName glyphRefID="3" NameString="space" />

  <!-- start of Emoji source glyph name assignments -->
"""

POST_FOOTER = u"""</postTable>
"""

CMAP_HEADER = u"""<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<!DOCTYPE cmapTable [
<!ELEMENT cmapTable ((cmapSubtable|cmapUVSSubtable)+)>
<!ELEMENT cmapSubtable ((map | rangeMap)+)>
<!ELEMENT cmapUVSSubtable (variationSelectorRecord+)>
<!ELEMENT variationSelectorRecord ((defaultTable?), (nonDefaultTable?))>
<!ELEMENT defaultTable (unmappedCharacter+)>
<!ELEMENT nonDefaultTable (map+)>
<!ELEMENT unmappedCharacter EMPTY>
<!ELEMENT map EMPTY>
<!ELEMENT rangeMap EMPTY>
<!ATTLIST cmapTable versionMajor CDATA #IMPLIED versionMinor CDATA #IMPLIED>
<!ATTLIST cmapSubtable encodingID CDATA #IMPLIED
    format CDATA #REQUIRED
    platformID CDATA #REQUIRED
    platformName CDATA #IMPLIED
    scriptID CDATA #REQUIRED
    scriptName CDATA #IMPLIED
    languageID CDATA #REQUIRED
    languageName CDATA #IMPLIED>
<!ATTLIST cmapUVSSubtable encodingID CDATA #IMPLIED
    format CDATA #IMPLIED
    length CDATA #IMPLIED
    platformID CDATA #REQUIRED
    platformName CDATA #IMPLIED
    scriptID CDATA #REQUIRED
    scriptName CDATA #IMPLIED
    numRecords CDATA #IMPLIED>
<!ATTLIST variationSelectorRecord variationSelector CDATA #REQUIRED
    variationSelectorName CDATA #IMPLIED
    defaultTableOffset CDATA #IMPLIED
    nonDefaultTableOffset CDATA #IMPLIED>
<!ATTLIST defaultTable numRanges CDATA #IMPLIED>
<!ATTLIST nonDefaultTable numMappings CDATA #IMPLIED>
<!ATTLIST unmappedCharacter charValue CDATA #REQUIRED charName CDATA #IMPLIED>
<!ATTLIST map charValue CDATA #REQUIRED
    charName CDATA #IMPLIED
    glyphRefID CDATA #REQUIRED
    glyphName CDATA #IMPLIED>
<!ATTLIST rangeMap startCharValue CDATA #REQUIRED
    startCharName CDATA #IMPLIED
    endCharValue CDATA #REQUIRED
    endCharName CDATA #IMPLIED
    glyphRefID CDATA #REQUIRED
    glyphName CDATA #IMPLIED
    incrementGlyphID CDATA #IMPLIED>
]>

<cmapTable versionMajor="1" versionMinor="0">
  <cmapSubtable encodingID="0"
      format="4"
      platformID = "0" platformName="Unicode" scriptID="3"
      languageID="-1" languageName="No language">
    <map charValue="0x0000" glyphRefID="1"/>
    <map charValue="0x000C" glyphRefID="2"/>
    <map charValue="0x0020" glyphRefID="3"/>

    <!-- start of Emoji source unicode assignments --> 
"""

CMAP_FOOTER = u"""  </cmapSubtable>
</cmapTable>
"""

def _WriteFontDB(writer):
  category_number = 0
  for category in emoji4unicode.GetCategories():
    category_number += 1
    for subcategory in category.GetSubcategories():
      for symbol in subcategory.GetSymbols():
        glyph_id = symbol.GetGlyphRefID()
        if glyph_id:
          if symbol.in_proposal and not symbol.GetUnicode():
            design = symbol.GetDesign()
          else:
            design = "**Symbol no longer proposed for new encoding**"
          writer.write(u"%d\tE%s\t%d\t%s\t%s\t%s\t%s\t%s\n" %
                       (glyph_id, symbol.id,
                        category_number, category.name[3:], subcategory.name,
                        symbol.GetName(),
                        symbol.GetDescription(), design))
  writer.close()


def _WritePostXML(writer):
  postscriptnames = []
  for symbol in emoji4unicode.GetSymbols():
    glyph_id = symbol.GetGlyphRefID()
    if glyph_id:
      if symbol.in_proposal and not symbol.GetUnicode():
        name = symbol.GetName().replace(" ", "_").replace("-", "_").lower()
        name = "uni" + symbol.GetFontUnicode() + "." + name
      else:
        name = ".notdef"
      postscriptnames.append((glyph_id, name))
  postscriptnames.sort()
  writer.write(POST_HEADER)
  for psn in postscriptnames:
    writer.write('  <PostScriptName glyphRefID="%d" NameString="%s" />\n' %
                  (psn[0], psn[1]))
  writer.write(POST_FOOTER)
  writer.close()


def _WriteCmapXML(writer):
  char_maps = []
  for symbol in emoji4unicode.GetSymbols():
    glyph_id = symbol.GetGlyphRefID()
    if glyph_id and symbol.in_proposal and not symbol.GetUnicode():
      char_maps.append((symbol.GetFontUnicode(), glyph_id))
  char_maps.sort()
  writer.write(CMAP_HEADER)
  for char_map in char_maps:
    writer.write('    <map charValue="0x%s" glyphRefID="%d"/>\n' %
                  (char_map[0], char_map[1]))
  writer.write(CMAP_FOOTER)
  writer.close()


def main():
  emoji4unicode.Load()
  here = os.path.dirname(__file__)
  filename = os.path.join(here, "..", "generated", "font_db.txt")
  _WriteFontDB(codecs.open(filename, "w", "UTF-8"))
  filename = os.path.join(here, "..", "generated", "emoji_post_source.xml")
  _WritePostXML(codecs.open(filename, "w", "UTF-8"))
  filename = os.path.join(here, "..", "generated", "emoji_cmap_source.xml")
  _WriteCmapXML(codecs.open(filename, "w", "UTF-8"))


if __name__ == "__main__":
  main()
