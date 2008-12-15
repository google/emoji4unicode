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

def _WriteFontDB(writer):
  category_number = 0
  for category in emoji4unicode.GetCategories():
    category_number += 1
    for subcategory in category.GetSubcategories():
      for symbol in subcategory.GetSymbols():
        glyph_id = symbol.GetGlyphRefID()
        if glyph_id:
          writer.write(u"%d\tE%s\t%d\t%s\t%s\t%s\t%s\t%s\n" %
                       (glyph_id, symbol.id,
                        category_number, category.name[3:], subcategory.name,
                        symbol.GetName(),
                        symbol.GetDescription(), symbol.GetDesign()))


def main():
  emoji4unicode.Load()
  here = os.path.dirname(__file__)
  filename = os.path.join(here, "..", "generated", "font_db.txt")
  _WriteFontDB(codecs.open(filename, "w", "UTF-8"))


if __name__ == "__main__":
  main()
