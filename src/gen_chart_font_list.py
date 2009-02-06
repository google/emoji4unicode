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

"""Generate the chart font list (CFL) file for Emoji chart printing."""

__author__ = "Markus Scherer"

import codecs
import datetime
import os.path
import emoji4unicode

_date = datetime.date.today().strftime("%Y-%m-%d")

_HEADER = """; Emoji chart font list (CFL) file
; Date: """ + _date + """

"""

def _WriteChartFontListFile(writer):
  writer.write(_HEADER)
  symbols = emoji4unicode.GetSymbolsInProposalSortedByUnicode()
  first_code_point = 0
  first_font_code_point = 0
  prev_code_point = 0
  prev_font_code_point = 0
  for symbol in symbols:
    code_points = symbol[0]
    symbol = symbol[1]
    if symbol.GetUnicode() or len(code_points) != 1: continue
    code_point = code_points[0]
    font_code_point = int(symbol.GetFontUnicode(), 16)
    if ((code_point != (prev_code_point + 1)) or
        (font_code_point != (prev_font_code_point + 1))):
      if prev_code_point:
        writer.write(u"Apple Emoji, 24 /Q=%04X /R=%04X-%04X\n" %
                     (first_code_point, first_font_code_point, prev_font_code_point))
      first_code_point = code_point
      first_font_code_point = font_code_point
    prev_code_point = code_point
    prev_font_code_point = font_code_point
  if prev_code_point:
    writer.write(u"Apple Emoji, 24 /Q=%04X /R=%04X-%04X\n" %
                  (first_code_point, first_font_code_point, prev_font_code_point))
  writer.close()


def main():
  emoji4unicode.Load()
  here = os.path.dirname(__file__)
  filename = os.path.join(here, "..", "generated", "emoji_cfl.txt")
  _WriteChartFontListFile(codecs.open(filename, "w", "UTF-8"))


if __name__ == "__main__":
  main()
