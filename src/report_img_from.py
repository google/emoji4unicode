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

"""Report which carrier's images we use for the symbol representation.

Exclude symbols that are not part of the proposal, or that are unified with
existing characters.
"""

__author__ = "Markus Scherer"

import cgi
import codecs
import sys
import carrier_data
import emoji4unicode
import utf

def main():
  emoji4unicode.Load()
  docomo_data = emoji4unicode.all_carrier_data["docomo"]
  img_from_counts = {"docomo":0, "kddi":0, "softbank":0, "google":0}
  docomo_exp = 0
  only_docomo_exp = 0
  for symbol in emoji4unicode.GetSymbols():
    if not symbol.in_proposal: continue
    if symbol.GetUnicode(): continue
    img_from = symbol.ImageFromWhichCarrier()
    img_from_counts[img_from] += 1
    if img_from == "docomo":
      docomo_uni = symbol.GetCarrierUnicode("docomo")
      docomo_symbol = docomo_data.SymbolFromUnicode(docomo_uni)
      if docomo_symbol.number >= 300:  # Expansion Pictogram
        docomo_exp += 1
        has_kddi = False
        kddi_uni = symbol.GetCarrierUnicode("kddi")
        if kddi_uni and not kddi_uni.startswith(">"):
          has_kddi = True
        has_softbank = False
        softbank_uni = symbol.GetCarrierUnicode("softbank")
        if softbank_uni and not softbank_uni.startswith(">"):
          has_softbank = True
        msg = "e-%s img_from=docomo" % symbol.id
        if not has_kddi and not has_softbank:
          msg += " Expansion Pictogram only"
          only_docomo_exp += 1
        else:
          if has_kddi: msg += ", kddi available"
          if has_softbank: msg += ", softbank available"
        print msg
  print "Number of symbol images from which carrier:"
  print img_from_counts
  print ("Number of symbol images from DoCoMo Expansion Pictograms: %d" %
         docomo_exp)
  print ("Number of these symbol images where there are no KDDI or SoftBank "
         "round-trip mappings: %d" %
         only_docomo_exp)

if __name__ == "__main__":
  main()
