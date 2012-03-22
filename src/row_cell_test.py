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
import row_cell

class RowCellTest(unittest.TestCase):
  def testInit(self):
    rc = row_cell.RowCell(1, 94)
    self.assertEqual(rc.row, 1)
    self.assertEqual(rc.cell, 94)
    self.assertRaises(ValueError, row_cell.RowCell, 0, 94)
    self.assertRaises(ValueError, row_cell.RowCell, 95, 94)
    self.assertRaises(ValueError, row_cell.RowCell, 1, 0)
    self.assertRaises(ValueError, row_cell.RowCell, 1, 95)

  def testString(self):
    self.assertEqual(str(row_cell.RowCell(1, 94)), "015E")

  def testToDecimalString(self):
    self.assertEqual(row_cell.RowCell(1, 94).ToDecimalString(), "0194")

  def testCmp(self):
    rc1122 = row_cell.RowCell(11, 22)
    rc2222 = row_cell.RowCell(22, 22)
    rc2223 = row_cell.RowCell(22, 23)
    self.assert_(rc1122.__cmp__(rc1122) == 0)
    self.assert_(rc1122.__cmp__(rc2222) < 0)
    self.assert_(rc2222.__cmp__(rc1122) > 0)
    self.assert_(rc2222.__cmp__(rc2223) < 0)
    self.assert_(rc2223.__cmp__(rc2222) > 0)

  def testAdd(self):
    rc = row_cell.FromDecimalString("9393")
    self.assertRaises(ValueError, rc.__add__, -1)
    self.assertEqual(rc + 0, row_cell.RowCell(93, 93))
    self.assertEqual(rc + 1, row_cell.RowCell(93, 94))
    self.assertEqual(rc + 2, row_cell.RowCell(94, 01))
    self.assertEqual(rc + 95, row_cell.RowCell(94, 94))
    self.assertRaises(OverflowError, rc.__add__, 96)

  def testSub(self):
    rc2122 = row_cell.RowCell(21, 22)
    rc2222 = row_cell.RowCell(22, 22)
    rc2223 = row_cell.RowCell(22, 23)
    self.assertEqual(rc2122 - rc2122, 0)
    self.assertEqual(rc2223 - rc2222, 1)
    self.assertEqual(rc2222 - rc2223, -1)
    self.assertEqual(rc2223 - rc2122, 95)
    self.assertEqual(rc2122 - rc2223, -95)

  def testFromHexString(self):
    rc = row_cell.FromHexString("015E")
    self.assertEqual(rc, row_cell.RowCell(1, 94))
    self.assertRaises(ValueError, row_cell.FromHexString, "")
    self.assertRaises(ValueError, row_cell.FromHexString, "01")
    self.assertRaises(ValueError, row_cell.FromHexString, "015E.")
    self.assertRaises(ValueError, row_cell.FromHexString, "005E")
    self.assertRaises(ValueError, row_cell.FromHexString, "015F")

  def testFromDecimalString(self):
    rc = row_cell.FromDecimalString("0194")
    self.assertEqual(rc, row_cell.RowCell(1, 94))
    self.assertRaises(ValueError, row_cell.FromDecimalString, "")
    self.assertRaises(ValueError, row_cell.FromDecimalString, "01")
    self.assertRaises(ValueError, row_cell.FromDecimalString, "0194.")
    self.assertRaises(ValueError, row_cell.FromDecimalString, "0094")
    self.assertRaises(ValueError, row_cell.FromDecimalString, "0195")

  def testFrom2022(self):
    rc = row_cell.From2022(0x21, 0x7e)
    self.assertEqual(rc, row_cell.RowCell(1, 94))
    self.assertRaises(ValueError, row_cell.From2022, 0x20, 0x7e)
    self.assertRaises(ValueError, row_cell.From2022, 0x21, 0x7f)

  def testTo2022(self):
    self.assertEqual(row_cell.RowCell(1, 1).To2022(), (0x21, 0x21))
    self.assertEqual(row_cell.RowCell(93, 94).To2022(), (0x7d, 0x7e))

  def testFrom2022Integer(self):
    rc = row_cell.From2022Integer(0x217e)
    self.assertEqual(rc, row_cell.RowCell(1, 94))
    self.assertRaises(ValueError, row_cell.From2022Integer, 0x207e)
    self.assertRaises(ValueError, row_cell.From2022Integer, 0x217f)

  def testFrom2022String(self):
    rc = row_cell.From2022String("217E")
    self.assertEqual(rc, row_cell.RowCell(1, 94))
    self.assertRaises(ValueError, row_cell.From2022String, "")
    self.assertRaises(ValueError, row_cell.From2022String, "21")
    self.assertRaises(ValueError, row_cell.From2022String, "217E.")
    self.assertRaises(ValueError, row_cell.From2022String, "207E")
    self.assertRaises(ValueError, row_cell.From2022String, "217F")

  def testFromShiftJis(self):
    rc = row_cell.FromShiftJis(0x81, 0x40)
    self.assertEqual(rc, row_cell.RowCell(1, 1))
    rc = row_cell.FromShiftJis(0xef, 0xfc)
    self.assertEqual(rc, row_cell.RowCell(94, 94))
    self.assertRaises(ValueError, row_cell.FromShiftJis, 0x80, 0x40)
    self.assertRaises(ValueError, row_cell.FromShiftJis, 0xa0, 0x40)
    self.assertRaises(ValueError, row_cell.FromShiftJis, 0xf0, 0x40)
    self.assertRaises(ValueError, row_cell.FromShiftJis, 0x81, 0x3f)
    self.assertRaises(ValueError, row_cell.FromShiftJis, 0x81, 0x7f)
    self.assertRaises(ValueError, row_cell.FromShiftJis, 0x81, 0xfd)

  def testToShiftJis(self):
    sjis = row_cell.RowCell(1, 1).ToShiftJisString()
    self.assertEqual(sjis, "8140")
    sjis = row_cell.RowCell(94, 94).ToShiftJisString()
    self.assertEqual(sjis, "EFFC")

  def testFromShiftJisString(self):
    rc = row_cell.FromShiftJisString("819E")
    self.assertEqual(rc, row_cell.RowCell(1, 94))
    self.assertRaises(ValueError, row_cell.FromShiftJisString, "")
    self.assertRaises(ValueError, row_cell.FromShiftJisString, "81")
    self.assertRaises(ValueError, row_cell.FromShiftJisString, "819E.")
    self.assertRaises(ValueError, row_cell.FromShiftJisString, "809E")
    self.assertRaises(ValueError, row_cell.FromShiftJisString, "817F")


if __name__ == "__main__":
  unittest.main()
