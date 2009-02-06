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

def _WriteNamesList(writer):
  writer.write(_HEADER)
  symbols = emoji4unicode.GetSymbolsInProposalSortedByUnicode()
  prev_subcategory_name = ""
  for symbol in symbols:
    code_points = symbol[0]
    symbol = symbol[1]
    if symbol.GetUnicode(): continue
    if code_points == [0x1F300]:
      writer.write("@@\t1F300\tMiscellaneous Pictographic Symbols\t1F5FF\n")
    elif code_points == [0x1F600]:
      writer.write("@@\t1F600\tEmoji Compatibility Symbols\t1F67F\n")
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
  _WriteNamesList(codecs.open(filename, "w", "UTF-8"))


if __name__ == "__main__":
  main()
