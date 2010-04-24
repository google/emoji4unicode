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

"""Generate the NamesList.txt file for Emoji symbols."""

__author__ = "Markus Scherer"

import codecs
import datetime
import os.path
import emoji4unicode

_date = datetime.date.today().strftime("%Y-%m-%d")

_HEADER = """@@@\tEmoji Symbols
@@@+\t""" + _date + """
"""

_BLOCK_HEADINGS = {
  0x23E9: """
@@\t2300\tMiscellaneous Technical\t23FF
;; UTC: 2009-02-06
;; UTC: 2009-05-15 sync with Wg2 content
;; WG2: 2009-04-24
;; contact: Markus Scherer, German NB
;; document: N3582, N3583, L2/09-026, L2/09-021
;; font: Uni2300Mistechnical
;; target: Amd8

""",
  0x26CE: """
@@\t2600\tMiscellaneous Symbols\t26FF
;; UTC: 2009-02-06
;; UTC: 2009-05-15 sync with Wg2 content, added Pentagrams
;; WG2: 2009-04-24
;; WG2: 2009-10-28 add 26E7
;; WG2: 2010-04-22 remove A78F
;; contact: Markus Scherer, German NB, Azzeddine Lazrek
;; document: N3582, N3583, L2/09-026, L2/09-021, L2/09-185R2
;; font: Uni2600Miscsymbols
;; target: Amd8

""",
  0x2705: """
@@\t2700\tDingbats\t27BF
;; UTC: 2009-02-06
;; UTC: 2009-05-15 sync with Wg2 content
;; WG2: 2009-04-24
;; WG2: 2009-10-28 add 27B0 (from 2E32) 27BF
;; contact: Markus Scherer, German NB
;; document: N3582, N3583, L2/09-026, L2/09-021
;; font: Uni2600Miscsymbols
;; target: Amd8

""",
  0x2E32: """
@@\t2E00\tSupplemental Punctuation\t2E7F
;; UTC: 2009-02-06
;; WG2: $$$$
;; contact: Markus Scherer
;; document: Nxxxx, L2/09-026
;; font: Apple Emoji
;; target: Amd8

""",
  0x1F0CF: """
@@\t1F0A0\tPlaying Cards\t1F0FF
;; UTC: 2009-05-15
;; WG2: 2009-04-23
;; contact: Michael Everson
;; document: N3607
;; font: Uni1F0A0Playingcards
;; target: Amd8

""",
  0x1F170: """
@@\t1F100\tEnclosed Alphanumeric Supplement\t1F1FF
;; UTC: 2009-02-06 (original Emoji)
;; UTC: 2009-05-15 (sync with WG2)
;; WG2: 2009-04-24
;; WG2: 2009-10-29 Irish pdam8 ballot additions + regional indicators
;; contact: Markus Scherer, Michael Everson
;; document: N3582, N3583, L2/09-026, N3626, L2/09-173
;; font: Uni1F100Enclosedsupplement
;; target: Amd8

""",
  0x1F201: """
@@\t1F200\tEnclosed Ideographic Supplement\t1F2FF
;; UTC: 2009-02-06 (original Emoji)
;; UTC: 2009-05-15 (sync with WG2)
;; WG2: 2009-04-24
;; contact: Markus Scherer
;; document: N3582, N3583, L2/09-026, N3626, L2/09-173
;; font: Uni1F100Enclosedsupplement
;; target: Amd8

""",
  0x1F300: """
@@\t1F300\tMiscellaneous Symbols and Pictographs\t1F5FF
;; UTC: 2009-02-06 (original Emoji)
;; UTC: 2009-05-15 (Sync with WG2)
;; WG2: 2009-04-24
;; WG2: 2009-10-28
;; contact: Markus Scherer, Michael Everson
;; document: N3582, N3583, L2/09-026, N3626
;; font: Uni1F300Mispictographics
;; target: Amd8

""",
  0x1F601: """
@@\t1F600\tEmoticons\t1F64F
;; UTC: 2009-02-06 (original Emoji)
;; UTC: 2009-05-15 sync with WG2
;; WG2: 2009-04-24
;; WG2: 2009-10-28 after ballot
;; WG2: 2009-04-22 rearranged, 1F610 added
;; contact: Markus Scherer, Michael Everson
;; document: N3582, N3583, L2/09-026
;; font: Uni1F600Emoticons
;; target: Amd8

""",
  0x1F680: """
@@\t1F680\tTransport and Map symbols\t1F6FF
;; UTC: 2009-02-06 (original Emoji)
;; UTC: 2009-05-15 sync with Wg2 content
;; WG2: 2099-04-24
;; WG2: 2009-10-28 after ballot
;; contact: Markus Scherer, Michael Everson
;; document: N3582, N3583, L2/09-026
;; font: Uni1F680Transport
;; target: Amd8

"""}

def _WriteNamesList(writer):
  writer.write(_HEADER)
  symbols = emoji4unicode.GetSymbolsInProposalSortedByUnicode()
  prev_subcategory_name = ""
  for symbol in symbols:
    code_points = symbol[0]
    symbol = symbol[1]
    if symbol.GetUnicode(): continue
    block_heading = _BLOCK_HEADINGS.get(code_points[0])
    if block_heading: writer.write(block_heading)
    subcategory_name = symbol.subcategory.name
    if prev_subcategory_name != subcategory_name:
      writer.write("\n@\t\t%s\n" % subcategory_name)
      prev_subcategory_name = subcategory_name
    uni = symbol.GetProposedUnicode()
    writer.write("%s\t%s\n" % (uni, symbol.GetName()))
    for line in symbol.GetAnnotations():
      writer.write("\t%s\n" % line)
    writer.write(";\t= e-%s\n" % symbol.id)
  writer.close()


def main():
  emoji4unicode.Load()
  here = os.path.dirname(__file__)
  filename = os.path.join(here, "..", "generated", "NamesList.txt")
  _WriteNamesList(codecs.open(filename, "w", "ISO-8859-1"))


if __name__ == "__main__":
  main()
