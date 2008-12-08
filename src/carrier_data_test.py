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

import unittest
import carrier_data

class DocomoDataTest(unittest.TestCase):
  def setUp(self):
    self.__data = carrier_data.GetDocomoData()

  def testMappings(self):
    symbol_e640 = self.__data.SymbolFromUnicode("E640")
    self.assertEqual(symbol_e640.uni, "E640")
    self.assertEqual(symbol_e640.number, 3)
    self.assertEqual(symbol_e640.shift_jis, "F8A1")
    self.assertEqual(symbol_e640.jis, "7545")
    self.assertEqual(symbol_e640.GetEnglishName(), "Rain")
    self.assertEqual(symbol_e640.GetJapaneseName(), u"\u96e8")

  def testAllUni(self):
    all_uni = self.__data.all_uni
    self.assertEqual(len(all_uni), 282)
    self.failIf("E63D" in all_uni)
    self.assert_("E63E" in all_uni)
    self.assert_("E6FE" in all_uni)
    self.assert_("E757" in all_uni)
    self.failIf("E758" in all_uni)


class KddiDataTest(unittest.TestCase):
  def setUp(self):
    self.__data = carrier_data.GetKddiData()

  def testMappings(self):
    symbol_e481 = self.__data.SymbolFromUnicode("E481")
    self.assertEqual(symbol_e481.uni, "E481")
    self.assertEqual(symbol_e481.number, 1)
    self.assertEqual(symbol_e481.shift_jis, "F659")
    self.assertEqual(symbol_e481.jis, "753A")
    self.assertEqual(symbol_e481.GetEnglishName(), "")
    self.assertEqual(symbol_e481.GetJapaneseName(), u"\uff01")
    self.assertEqual(symbol_e481.ImageHTML(),
                     "<img src=http://www001.upp.so-net.ne.jp/hdml/emoji/e/"
                     "1.gif>")

    symbol_e513 = self.__data.SymbolFromUnicode("E513")
    self.assertEqual(symbol_e513.uni, "E513")
    self.assertEqual(symbol_e513.number, 53)
    self.assertEqual(symbol_e513.shift_jis, "F6EC")
    self.assertEqual(symbol_e513.jis, "766E")
    self.assertEqual(symbol_e513.GetEnglishName(), "")
    self.assertEqual(symbol_e513.GetJapaneseName(), u"\u56db\u3064\u8449")
    self.assertEqual(symbol_e513.ImageHTML(),
                     "<img src=http://www001.upp.so-net.ne.jp/hdml/emoji/e/"
                     "53.gif>")

  def testAllUni(self):
    all_uni = self.__data.all_uni
    self.assertEqual(len(all_uni), 647)
    self.assert_("E468" in all_uni)
    self.failIf("EA7F" in all_uni)
    self.assert_("EA88" in all_uni)
    self.assert_("EB8E" in all_uni)


class SoftbankDataTest(unittest.TestCase):
  def setUp(self):
    self.__data = carrier_data.GetSoftbankData()

  def testMappings(self):
    symbol_e53e = self.__data.SymbolFromUnicode("E53E")
    self.assertEqual(symbol_e53e.uni, "E53E")
    self.assertEqual(symbol_e53e.number, None)
    self.assertEqual(symbol_e53e.old_number, 485)
    self.assertEqual(symbol_e53e.new_number, None)
    self.assertEqual(symbol_e53e.shift_jis, "FBDE")
    self.assertEqual(symbol_e53e.jis, None)  # "7D77"
    self.assertEqual(symbol_e53e.GetEnglishName(), "")
    self.assertEqual(symbol_e53e.GetJapaneseName(), "vodafone5")

    symbol_e11c = self.__data.SymbolFromUnicode("E11C")
    self.assertEqual(symbol_e11c.number, 299)
    self.assertEqual(symbol_e11c.old_number, 118)
    self.assertEqual(symbol_e11c.new_number, None)

  def testAllUni(self):
    all_uni = self.__data.all_uni
    self.assertEqual(len(all_uni), 485)
    self.assert_("E001" in all_uni)
    self.assert_("E15A" in all_uni)
    self.failIf("E15B" in all_uni)
    self.assert_("E53E" in all_uni)


class GoogleDataTest(unittest.TestCase):
  def setUp(self):
    self.__data = carrier_data.GetGoogleData()

  def testMappings(self):
    symbol_fe001 = self.__data.SymbolFromUnicode("FE001")
    self.assertEqual(symbol_fe001.uni, "FE001")
    self.assertEqual(symbol_fe001.number, None)
    self.assertEqual(symbol_fe001.shift_jis, None)
    self.assertEqual(symbol_fe001.jis, None)
    self.assertEqual(symbol_fe001.GetEnglishName(), "")
    self.assertEqual(symbol_fe001.GetJapaneseName(), "")


if __name__ == "__main__":
  unittest.main()
