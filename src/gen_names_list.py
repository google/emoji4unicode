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
;; WG2: --
;; contact: Markus Scherer
;; document: Nxxxx, L2/09-026
;; font: --
;; target: Amd7

""",
  0x2705: """
@@\t2700\tDingbats\t27BF
;; UTC: 2009-02-06
;; WG2: --
;; contact: Markus Scherer, German NB
;; document: Nxxxx, L2/09-021
;; font: --
;; target: Amd7

""",
  0x2E32: """
@@\t2E00\tSupplemental Punctuation\t2E7F
;; UTC: 2009-02-06
;; WG2: --
;; contact: Markus Scherer
;; document: Nxxxx, L2/09-026
;; font: --
;; target: Amd7

""",
  0x1F201: """
@@\t1F200\tEnclosed Ideographic Supplement\t1F2FF
;; UTC: 2009-02-06
;; WG2: --
;; contact: Markus Scherer
;; document: L2/09-026
;; font: --
;; target: Amd7

""",
  0x1F300: """
@@\t1F300\tMiscellaneous Pictographic Symbols\t1F5FF
;; UTC: 2009-02-06
;; WG2: --
;; contact: Markus Scherer
;; document: L2/09-026
;; font: --
;; target: Amd7

""",
  0x1F600: """
@@\t1F600\tEmoji Compatibility Symbols\t1F67F
;; UTC: 2009-02-06
;; WG2: --
;; contact: Markus Scherer
;; document: L2/09-026
;; font: --
;; target: Amd7

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
      writer.write("@\t\t%s\n" % subcategory_name)
      prev_subcategory_name = subcategory_name
    uni = symbol.GetProposedUnicode()
    writer.write("%s\t%s\n" % (uni, symbol.GetName()))
    for line in symbol.GetAnnotations():
      writer.write("\t%s\n" % line)
  writer.close()


def main():
  emoji4unicode.Load()
  here = os.path.dirname(__file__)
  filename = os.path.join(here, "..", "generated", "NamesList.txt")
  _WriteNamesList(codecs.open(filename, "w", "ISO-8859-1"))


if __name__ == "__main__":
  main()
