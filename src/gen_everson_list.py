#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
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

"""Generate a text file with good/neutral/bad changes made by N3607
or successor documents."""

__author__ = "Markus Scherer"

import codecs
import datetime
import os.path
import emoji4unicode
import everson

_date = datetime.date.today().strftime("%Y-%m-%d")

_HEADER = "Comments on specific changes suggested by " + everson.doc + """
                                                           N36xx
                                                           L2/09-xxx
                                           """ + _date + """
                                           Authors:
                                           Markus Scherer, Mark Davis, Kat Momoi
"""

def _WriteList(writer):
  writer.write(_HEADER)
  # Glyph changes.
  writer.write(u"""
## Glyph changes proposed in """ + everson.doc + u"""
## We have reviewed the substantive glyph changes proposed in """ +
everson.doc + u"""
## for the following characters and made a preliminary assessment.
## The glyph changes for other characters are more difficult to evaluate
## and are still being reviewed.
""")
  symbols = everson.GetGoodGlyphChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"\n# Good glyph changes (%d)\n" % len(symbols))
    _WriteGlyphChanges(writer, symbols)
  symbols = everson.GetNeutralGlyphChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"\n# Neutral glyph changes (%d)\n" % len(symbols))
    _WriteGlyphChanges(writer, symbols)
  symbols = everson.GetSomewhatBadGlyphChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"\n# Somewhat bad glyph changes (%d)\n" % len(symbols))
    _WriteGlyphChanges(writer, symbols)
  symbols = everson.GetBadGlyphChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"\n# Bad glyph changes (%d)\n" % len(symbols))
    _WriteGlyphChanges(writer, symbols)
  # Name changes.
  writer.write(u"""
## Name changes proposed in """ + everson.doc + u"""
## We have reviewed the name changes proposed in """ + everson.doc + u"""
## for the following characters and made a preliminary assessment.
## The name changes for other characters are more difficult to evaluate
## and are still being reviewed.
""")
  symbols = everson.GetGoodNameChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"\n# Good name changes (%d)\n" % len(symbols))
    _WriteNameChanges(writer, symbols)
  symbols = everson.GetNeutralNameChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"\n# Neutral name changes (%d)\n" % len(symbols))
    _WriteNameChanges(writer, symbols)
  symbols = everson.GetBadNameChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"\n# Bad name changes (%d)\n" % len(symbols))
    _WriteNameChanges(writer, symbols)


def _WriteGlyphChanges(writer, symbols):
  writer.write(u"# ID\tN3582\t" + everson.doc + u"\tName\n")
  for symbol in symbols:
    proposed_uni = symbol.GetProposedUnicode()
    writer.write(u"e-%s\t%s\t%s\t%s\n" %
                 (symbol.id, proposed_uni,
                  everson.GetUnicode(proposed_uni), symbol.GetName()))


def _WriteNameChanges(writer, symbols):
  writer.write(u"# ID\tN3582\tName\n")
  writer.write(u"#\t" + everson.doc + u"\tName\n")
  for symbol in symbols:
    proposed_uni = symbol.GetProposedUnicode()
    writer.write(u"e-%s\t%s\t%s\n" %
                 (symbol.id, proposed_uni, symbol.GetName()))
    writer.write(u"\t%s\t%s\n" %
                 (everson.GetUnicode(proposed_uni),
                  everson.GetName(proposed_uni)))


def main():
  emoji4unicode.Load()
  everson.Load()
  here = os.path.dirname(__file__)
  filename = os.path.join(here, "..", "generated",
                          everson.doc.lower() + "_compare.txt")
  _WriteList(codecs.open(filename, "w", "UTF-8"))


if __name__ == "__main__":
  main()
