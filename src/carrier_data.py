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

"""Cell phone carrier Emoji symbols data loading and access."""

__author__ = "Markus Scherer"

import os.path
import xml.dom.minidom
import row_cell

class CarrierData(object):
  """One carrier's Emoji symbols data.

  Attributes:
    all_uni: All Unicode code points, for all of this carrier's symbols.
  """
  all_uni = frozenset()

  # Each _ranges attribute is a list of range tuples for mapping between
  # linear ranges of Unicode code points and corresponding linear, same-length
  # ranges of target values.
  # Shift-JIS or JIS target values only count valid codes according to the
  # encoding scheme.
  # See _RangeFromUnicode(), _NumberFromUnicode(), etc.
  _uni_to_number_ranges = None
  _uni_to_old_number_ranges = None
  _uni_to_shift_jis_ranges = None
  _uni_to_jis_ranges = None
  # Map from Unicode code point hex-digit strings to <e> DOM element nodes
  # with symbol data.
  _uni_to_elements = {}

  def _AllUnicodesFromRanges(self, ranges):
    """Build the all_uni set from a list of range tuples."""
    all_uni = set()
    for one_range in ranges:
      for uni in range(one_range[0], one_range[1] + 1):
        all_uni.add("%04X" % uni)
    self.all_uni = frozenset(all_uni)

  def _CheckRanges(self):
    """Verify that in each range tuple the source and target ranges
    have the same length."""
    if self._uni_to_number_ranges:
      for range in self._uni_to_number_ranges:
        assert (range[1] - range[0]) == (range[3] - range[2])
    if self._uni_to_old_number_ranges:
      for range in self._uni_to_old_number_ranges:
        assert (range[1] - range[0]) == (range[3] - range[2])
    if self._uni_to_shift_jis_ranges:
      for range in self._uni_to_shift_jis_ranges:
        # Shift the Shift-JIS codes down to JIS X 0208 and compute the
        # linear differences.
        shift_jis_start = row_cell.FromShiftJis((range[2] >> 8) - 0x10,
                                                range[2] & 0xff)
        shift_jis_end = row_cell.FromShiftJis((range[3] >> 8) - 0x10,
                                              range[3] & 0xff)
        assert (range[1] - range[0]) == (shift_jis_end - shift_jis_start)
    if self._uni_to_jis_ranges:
      for range in self._uni_to_jis_ranges:
        jis_start = row_cell.From2022((range[2] >> 8), range[2] & 0xff)
        jis_end = row_cell.From2022((range[3] >> 8), range[3] & 0xff)
        assert (range[1] - range[0]) == (jis_end - jis_start)

  def _ReadXML(self, filename):
    self.__doc = xml.dom.minidom.parse(filename)
    self.__root = self.__doc.documentElement
    for element in self.__root.getElementsByTagName("e"):
      self._uni_to_elements[element.getAttribute("unicode")] = element

  def SymbolFromUnicode(self, uni):
    """Get carrier data for one Emoji symbol.

    Args:
      uni: Carrier Unicode PUA code point, as a hex digit string.

    Returns:
      The Symbol instance corresponding to uni.
    """
    symbol = Symbol()
    symbol.uni = uni
    symbol._element = self._uni_to_elements.get(uni)
    symbol._carrier_data = self

    if self._uni_to_number_ranges:
      symbol.number = _NumberFromUnicode(self._uni_to_number_ranges, uni)
    elif symbol._element:
      number = symbol._element.getAttribute("number")
      if number: symbol.number = int(number)

    if self._uni_to_old_number_ranges:
      symbol.old_number = _NumberFromUnicode(self._uni_to_old_number_ranges,
                                             uni)
    elif symbol._element:
      old_number = symbol._element.getAttribute("old_number")
      if old_number: symbol.old_number = int(old_number)

    if self._uni_to_shift_jis_ranges:
      symbol.shift_jis = (
          "%04X" % _ShiftJisFromUnicode(self._uni_to_shift_jis_ranges, uni))
    elif symbol._element:
      shift_jis = symbol._element.getAttribute("shift_jis")
      if shift_jis: symbol.shift_jis = shift_jis

    if self._uni_to_jis_ranges:
      symbol.jis = "%04X" % _JisFromUnicode(self._uni_to_jis_ranges, uni)
    elif symbol._element:
      jis = symbol._element.getAttribute("jis")
      if jis: symbol.jis = jis

    if symbol._element:
      new_number = symbol._element.getAttribute("new_number")
      if new_number: symbol.new_number = int(new_number)

    return symbol

  def _ImageHTML(self, uni, number):
    """Get HTML for the symbol image, or an empty string.

    Called only from Symbol.ImageHTML()."""
    return ""

  def GetShiftJISLeadBytes(self):
    """Returns a frozenset of Shift-JIS lead bytes for Emoji symbols."""
    lead_bytes = set()
    if self._uni_to_shift_jis_ranges:
      for sj_range in self._uni_to_shift_jis_ranges:
        lead_bytes |= set(range(sj_range[2] >> 8, (sj_range[3] >> 8) + 1))
    else:
      for element in self._uni_to_elements.itervalues():
        shift_jis = element.getAttribute("shift_jis")
        if shift_jis: lead_bytes.add(int(shift_jis[0:2], 16))
    return frozenset(lead_bytes)

  def GetJISLeadBytesAsShiftJIS(self):
    """Returns a frozenset of JIS lead bytes in Shift-JIS format."""
    lead_bytes = set()
    if self._uni_to_jis_ranges:
      for jis_range in self._uni_to_jis_ranges:
        sjis_start = row_cell.From2022Integer(jis_range[2]).ToShiftJis()
        sjis_end = row_cell.From2022Integer(jis_range[3]).ToShiftJis()
        lead_bytes |= set(range(sjis_start[0], sjis_end[0] + 1))
    else:
      for element in self._uni_to_elements.itervalues():
        jis = element.getAttribute("jis")
        if jis: lead_bytes.add(row_cell.From2022String(jis).ToShiftJis()[0])
    return frozenset(lead_bytes)

def _RangeFromUnicode(ranges, uni):
  """Select from a list the range containing the Unicode code point.

  Args:
    ranges: A list of ranges. Each range pair is a 4-tuple of
      (unicode_start, unicode_end, target_start, target_end) integers.
      Each range tuple represents a linear mapping between a range of Unicode
      code points and a range of numbers/Shift-JIS codes/JIS codes.
      In each tuple, the Unicode and target ranges must have the same length.
      The _end values are inclusive range boundaries.
    uni: A Unicode code point integer.

  Returns:
    The range tuple where unicode_start <= uni <= unicode_end.
  """
  for range in ranges:
    if range[0] <= uni <= range[1]: return range
  return None


def _NumberFromUnicode(ranges, uni):
  """Map a Unicode code point to a number.

  Args:
    ranges: A list of ranges. See _RangeFromUnicode().
    uni: A Unicode code point (a hex digit string).

  Returns:
    The number integer corresponding to the
    Unicode code point, according to the ranges;
    or None if none of the ranges contains the code point.
  """
  uni = int(uni, 16)
  range = _RangeFromUnicode(ranges, uni)
  return range[2] + (uni - range[0])


def _ShiftJisFromUnicode(ranges, uni):
  """Map a Unicode code point to a Shift-JIS code.

  In a range of Shift-JIS codes, only valid codes according to the encoding
  scheme are counted. For example, after F27E follows F280 because 7F is not
  a valid trail byte.

  Args:
    ranges: A list of ranges. See _RangeFromUnicode().
    uni: A Unicode code point (a hex digit string).

  Returns:
    The Shift-JIS code (integer) corresponding to the
    Unicode code point, according to the ranges;
    or None if none of the ranges contains the code point.
  """
  uni = int(uni, 16)
  range = _RangeFromUnicode(ranges, uni)
  offset = uni - range[0]
  # Shift the Shift-JIS codes down to JIS X 0208 and back up
  # so that we get standard row-cell byte values (1..94) and can use RowCell.
  rc = row_cell.FromShiftJis((range[2] >> 8) - 0x10, range[2] & 0xff) + offset
  (b1, b2) = rc.ToShiftJis()
  return ((b1 + 0x10) << 8) | b2


def _JisFromUnicode(ranges, uni):
  """Map a Unicode code point to a JIS X 0208 (ISO-2022-JP) code.

  In a range of JIS codes, only valid codes according to the encoding
  scheme are counted. For example, after 757E follows 7621.

  Args:
    ranges: A list of ranges. See _RangeFromUnicode().
    uni: A Unicode code point (a hex digit string).

  Returns:
    The JIS code (integer) corresponding to the
    Unicode code point, according to the ranges;
    or None if none of the ranges contains the code point.
  """
  uni = int(uni, 16)
  range = _RangeFromUnicode(ranges, uni)
  offset = uni - range[0]
  rc = row_cell.From2022(range[2] >> 8, range[2] & 0xff) + offset
  (b1, b2) = rc.To2022()
  return (b1 << 8) | b2


class Symbol(object):
  """Carrier data for one Emoji symbol."""
  __slots__ = ("uni", "number", "old_number", "new_number",
               "shift_jis", "jis", "_element", "_carrier_data")

  def __init__(self):
    """Carrier Emoji symbol data.

    Constructed by CarrierData.SymbolFromUnicode(). Do not instantiate yourself.

    Attributes:
      uni: Unicode PUA code point, 4..6-hex-digit string
      number: Carrier-specific Emoji symbol number
      old_number: Carrier-specific Emoji symbol number (old number system)
      new_number: Carrier-specific Emoji symbol number (new number system)
      shift_jis: Shift-JIS code, 4-hex-digit string
      jis: JIS (ISO-2022-JP) code, 4-hex-digit string
    """
    self.uni = None
    self.number = None
    self.old_number = None
    self.new_number = None
    self.shift_jis = None
    self.jis = None
    self._element = None  # <e> XML element

  def GetEnglishName(self):
    """Get the carrier's English name of this Emoji symbol."""
    if self._element:
      return self._element.getAttribute("name_en")
    else:
      return ""

  def GetJapaneseName(self):
    """Get the carrier's Japanese name of this Emoji symbol."""
    if self._element:
      return self._element.getAttribute("name_ja")
    else:
      return ""

  def ImageHTML(self):
    """Get HTML for the symbol image, or an empty string."""
    return self._carrier_data._ImageHTML(self.uni, self.number)


class _DocomoData(CarrierData):
  """DoCoMo Emoji symbols data."""
  _uni_to_number_ranges = [
      (0xE63E, 0xE6A5, 1, 104),
      (0xE6A6, 0xE6AB, 177, 182),
      (0xE6AC, 0xE6AE, 167, 169),
      (0xE6AF, 0xE6B0, 183, 184),
      (0xE6B1, 0xE6B3, 170, 172),
      (0xE6B4, 0xE6B6, 185, 187),
      (0xE6B7, 0xE6BA, 173, 176),
      (0xE6BB, 0xE6CD, 188, 206),
      (0xE6CE, 0xE6EB, 105, 134),
      (0xE6EC, 0xE70A, 136, 166),
      (0xE70B, 0xE70B, 135, 135),
      (0xE70C, 0xE757, 301, 376)]
  _uni_to_shift_jis_ranges = [(0xE63E, 0xE757, 0xF89F, 0xF9FC)]
  _uni_to_elements = {}

  def __init__(self):
    # TODO(mscherer): Add argument for root data folder path.
    filename = os.path.join(os.path.dirname(__file__),
                            "..", "data", "docomo", "carrier_data.xml")
    self._CheckRanges()
    self._AllUnicodesFromRanges(self._uni_to_shift_jis_ranges)
    self._ReadXML(filename)

  def _ImageHTML(self, uni, number):
    """Get HTML for the symbol image, or an empty string.

    Called only from Symbol.ImageHTML()."""
    path = "http://www.nttdocomo.co.jp/service/developer/make/content/pictograph/"
    if number < 300:
      return ("<img src=%sbasic/images/%d.gif width=16 height=16>" %
              (path, number))
    else:
      return ("<img src=%sextention/images/%d.gif width=16 height=16>" %
              (path, number - 300))


class _KddiData(CarrierData):
  """KDDI Emoji symbols data."""
  _uni_to_shift_jis_ranges = [
      (0xE468, 0xE5B4, 0xF640, 0xF7D1),
      (0xE5B5, 0xE5CC, 0xF7E5, 0xF7FC),
      (0xE5CD, 0xE5DF, 0xF340, 0xF352),
      (0xEA80, 0xEAFA, 0xF353, 0xF3CE),
      (0xEAFB, 0xEB0D, 0xF7D2, 0xF7E4),
      (0xEB0E, 0xEB8E, 0xF3CF, 0xF493)]
  _uni_to_jis_ranges = [
      (0xE468, 0xE5B4, 0x7521, 0x7853),
      (0xE5B5, 0xE5DF, 0x7867, 0x7933),
      (0xEA80, 0xEAFA, 0x7934, 0x7A50),
      (0xEAFB, 0xEB0D, 0x7854, 0x7866),
      (0xEB0E, 0xEB8E, 0x7A51, 0x7B73)]
  _uni_to_elements = {}

  def __init__(self):
    # TODO(mscherer): Add argument for root data folder path.
    filename = os.path.join(os.path.dirname(__file__),
                            "..", "data", "kddi", "carrier_data.xml")
    self._CheckRanges()
    self._AllUnicodesFromRanges(self._uni_to_shift_jis_ranges)
    self._ReadXML(filename)

  def _ImageHTML(self, uni, number):
    """Get HTML for the symbol image, or an empty string.

    Called only from Symbol.ImageHTML()."""
    return ("<img src=http://www001.upp.so-net.ne.jp/hdml/emoji/e/%d.gif>" %
            number)


class _SoftbankData(CarrierData):
  """SoftBank Emoji symbols data."""
  _uni_to_old_number_ranges = [
      (0xE001, 0xE05A, 1, 90),
      (0xE101, 0xE15A, 91, 180),
      (0xE201, 0xE25A, 181, 270),
      (0xE301, 0xE34D, 271, 347),
      (0xE401, 0xE44C, 348, 423),
      (0xE501, 0xE53E, 424, 485)]
  _uni_to_shift_jis_ranges = [
      (0xE001, 0xE05A, 0xF941, 0xF99B),
      (0xE101, 0xE15A, 0xF741, 0xF79B),
      (0xE201, 0xE25A, 0xF7A1, 0xF7FA),
      (0xE301, 0xE34D, 0xF9A1, 0xF9ED),
      (0xE401, 0xE44C, 0xFB41, 0xFB8D),
      (0xE501, 0xE53E, 0xFBA1, 0xFBDE)]
  _uni_to_elements = {}
  __animated_img = frozenset([
      "E101", "E102", "E103", "E104", "E105", "E106", "E107", "E108",
      "E10D", "E10F",
      "E113", "E115", "E117", "E11B", "E11D", "E12B", "E130",
      "E201", "E206", "E219", "E254", "E255", "E256", "E257", "E258",
      "E259", "E25A",
      "E30C", "E310", "E311", "E312", "E313", "E317", "E31E", "E31F",
      "E320", "E325", "E326", "E327", "E328", "E329", "E32E", "E335",
      "E336", "E337", "E34B",
      "E409", "E40D", "E412", "E417", "E41C", "E41E", "E41F", "E422",
      "E423", "E428", "E429", "E42D", "E433", "E437", "E43E", "E440",
      "E442", "E447", "E44B",
      "E51F", "E538", "E539", "E53A", "E53B", "E53C", "E53D", "E53E"])

  def __init__(self):
    # TODO(mscherer): Add argument for root data folder path.
    filename = os.path.join(os.path.dirname(__file__),
                            "..", "data", "softbank", "carrier_data.xml")
    self._CheckRanges()
    self._AllUnicodesFromRanges(self._uni_to_shift_jis_ranges)
    self._ReadXML(filename)

  def _ImageHTML(self, uni, number):
    """Get HTML for the symbol image, or an empty string.

    Called only from Symbol.ImageHTML()."""
    return ("<img src=http://creation.mb.softbank.jp/mc/tech/tech_pic/img/"
            "%s_20%s.gif>" %
            (uni,
             {False: "", True: "_ani"}[uni in self.__animated_img]))


class _GoogleData(CarrierData):
  """Google Emoji symbols data."""
  pass


# CarrierData singletons
_DOCOMO_DATA = None
_KDDI_DATA = None
_SOFTBANK_DATA = None
_GOOGLE_DATA = None

def GetDocomoData():
  global _DOCOMO_DATA
  if not _DOCOMO_DATA: _DOCOMO_DATA = _DocomoData()
  return _DOCOMO_DATA


def GetKddiData():
  global _KDDI_DATA
  if not _KDDI_DATA: _KDDI_DATA = _KddiData()
  return _KDDI_DATA


def GetSoftbankData():
  global _SOFTBANK_DATA
  if not _SOFTBANK_DATA: _SOFTBANK_DATA = _SoftbankData()
  return _SOFTBANK_DATA


def GetGoogleData():
  global _GOOGLE_DATA
  if not _GOOGLE_DATA: _GOOGLE_DATA = _GoogleData()
  return _GOOGLE_DATA
