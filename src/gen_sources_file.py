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

"""Generate the Emoji sources data file."""

__author__ = "Markus Scherer"

import codecs
import datetime
import os.path
import emoji4unicode

_date = datetime.date.today().strftime("%Y-%m-%d")

_HEADER = """# Emoji Sources
# N3835
#
# This is an updated version of N3728R, updated to reflect FDAM8
# which includes the disposition of FPDAM8 ballot comments and
# changes agreed during the San Jose WG2 meeting 56.
#
# Date: """ + _date + """
# Author: Markus Scherer
#
# This file provides mappings between UCS code points and sequences on one hand
# and Shift-JIS codes for cell phone carrier symbols on the other hand.
# Each mapping is symmetric ("round trip"), for equivalent UCS and carrier
# symbols or sequences. This file does not include best-fit ("fallback")
# mappings to similar but not equivalent symbols in either mapping direction.
#
# Note: It is possible that future versions of this file will include
# additional data columns providing mappings for additional vendors.
#
# Semicolon-delimited file with a fixed number of fields.
# The number of fields may increase in the future.
#
# Fields:
# 0: UCS code point or sequence
# 1: DoCoMo Shift-JIS code
# 2: KDDI Shift-JIS code
# 3: SoftBank Shift-JIS code
#
# Each field 1..3 contains a code if and only if the vendor character set
# has a symbol which is equivalent to the UCS character or sequence.

"""

def _WriteSourcesFile(writer):
  writer.write(_HEADER)
  symbols = emoji4unicode.GetSymbolsInProposalSortedByUnicode()
  for symbol in symbols:
    symbol = symbol[1]
    uni = symbol.GetUnicode()
    if not uni: uni = symbol.GetProposedUnicode()
    if uni == "27BF": continue  # Omit DOUBLE CURLY LOOP from sources file.
    fields = [uni.replace("+", " ")]
    has_mappings = False
    for carrier in ("docomo", "kddi", "softbank"):
      code = symbol.GetCarrierUnicode(carrier)
      if code and not code.startswith(">"):
        has_mappings = True
        one_carrier_data = emoji4unicode.all_carrier_data[carrier]
        carrier_symbol = one_carrier_data.SymbolFromUnicode(code)
        if carrier_symbol.shift_jis:
          fields.append(carrier_symbol.shift_jis)
        else:
          fields.append("Missing Shift-JIS code")
      else:
        fields.append("")
    if has_mappings: writer.write(u";".join(fields) + u"\n")
  writer.close()


def main():
  emoji4unicode.Load()
  here = os.path.dirname(__file__)
  filename = os.path.join(here, "..", "generated", "EmojiSrc.txt")
  _WriteSourcesFile(codecs.open(filename, "w", "UTF-8"))


if __name__ == "__main__":
  main()
