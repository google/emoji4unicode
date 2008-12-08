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

__author__ = "Markus Scherer"

import os.path
import unittest
import emoji4unicode
import ucm

class SourceSeparationTest(unittest.TestCase):
  def setUp(self):
    emoji4unicode.Load()
    here = os.path.dirname(__file__)
    filename = os.path.join(here, "..", "data", "icu", "windows-932-2000.ucm")
    self.__shift_jis_ucm = ucm.UCMFile(filename)

  def testShiftJis(self):
    """Check for source separation with standard Shift-JIS.

    No Unicode unification must be with a character from the JIS X 0208 part of
    Shift-JIS. This part has lead bytes below 0xF0.
    We consider only round-trip mappings because only those map the same
    characters between Unicode and Shift-JIS.
    (Fallbacks go to best-fit *similar* characters.)

    Japanese cell phone carriers encode Emoji symbols with Shift-JIS VDC codes.
    """
    errors = []
    for symbol in emoji4unicode.GetSymbols():
      uni = symbol.GetUnicode()
      if uni and uni in self.__shift_jis_ucm.round_trip_code_points:
        shift_jis = self.__shift_jis_ucm.from_unicode.get(uni)
        if shift_jis and shift_jis < "F":
          msg = ("source separation error: e-%s = U+%s = Shift-JIS-%s" %
                 (symbol.id, uni, shift_jis))
          print msg
          errors.append(msg)
    self.failIf(errors, errors)

  def testAllCarrierSymbols(self):
    """Verify that emoji4unicode.xml covers each carrier's set of symbols.

    Verify that we have exactly one round-trip mapping for each carrier's
    symbol.
    """
    # One set of symbol Unicode code points per carrier.
    # First we enumerate all symbols and each symbol's carrier mappings,
    # adding a round-trip mapping to the carrier's set.
    # Then we compare each carrier's set to CarrierData.all_uni.
    # They should match.
    carrier_all_uni = {"docomo": set(), "kddi": set(), "softbank": set()}
    carriers = carrier_all_uni.keys()
    for symbol in emoji4unicode.GetSymbols():
      for carrier in carriers:
        uni = symbol.GetCarrierUnicode(carrier)
        if uni and not uni.startswith(">"):
          self.failIf(uni in carrier_all_uni[carrier],
                      "emoji4unicode.xml has two round-trip mappings with "
                      "%s %s" % (carrier, uni))
          carrier_all_uni[carrier].add(uni)
    for carrier in carriers:
      e4u_set = carrier_all_uni[carrier]
      cd_set = emoji4unicode.all_carrier_data[carrier].all_uni
      self.assertEqual(e4u_set, cd_set,
                       "Mismatched all_uni sets for %s:\n"
                       "Missing from emoji4unicode.xml: %s\n"
                       "Missing from CarrierData: %s" %
                       (carrier, cd_set - e4u_set, e4u_set - cd_set))


if __name__ == "__main__":
  unittest.main()
