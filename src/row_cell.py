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

"""Represent, parse, format and convert row-cell character code values.

In ISO character set standards, row-cell value pairs are used for the encoding
of sets of a few thousands characters.
A row or cell value is a number 1..94=0x5e.

ISO-2022-* charsets add 0x20 to each value to get byte values 0x21..0x7e, for
"GL character sets".

EUC-* charsets add 0xa0 to each value to get byte values 0xa0..0xfe, for
"GR character sets".

Shift-JIS takes the 94x94 JIS X 0208 codes, 'shifts' them to a 47x188
configuration and adds various offsets to avoid certain lead and trail byte
values.

RowCell can only represent row-cell values corresponding to JIS X 0208,
limiting Shift-JIS codes to double-byte codes with lead bytes 81..9f and e0..ef,
excluding f0..fc.
"""

__author__ = "Markus Scherer"

class RowCell(object):
  """Row-cell value pair.

  Each of the two values is in the range 1..94.
  """
  __slots__ = "row", "cell"

  def __init__(self, row, cell):
    """Construct a RowCell from a pair of integers in the range 1..94.

    Args:
      row: Integer 1..94.
      cell: Integer 1..94.

    Raises:
      ValueError: One or both values are not 1..94.
    """
    if not 1 <= row <= 94 or not 1 <= cell <= 94:
      raise ValueError("row/cell (%d, %d) out of range" % (row, cell))
    self.row = row
    self.cell = cell

  def __str__(self):
    """Create a 4-hex-digit string from the row-cell values.

    >>> str(RowCell(1, 94))
    '015E'

    Returns: The 4-hex-digit string. Hex digits are uppercase.
    """
    return "%02X%02X" % (self.row, self.cell)

  def __cmp__(self, other):
    """Standard comparison method.

    Implements lexical result of the comparison of the row-cell pairs.

    Returns:
      negative/zero/positive integer corresponding to < == >
    """
    result = self.row.__cmp__(other.row)
    if result:
      return result
    else:
      return self.cell.__cmp__(other.cell)

  def __add__(self, other):
    """Create the other-th following RowCell.

    Args:
      other: A non-negative integer.

    Returns: The RowCell with a value pair which is 'other' values higher
      than this object's value pair.
    """
    if other < 0:
      raise ValueError("expect non-negative increment but got %d" % other)
    (row_inc, cell_rem) = divmod(self.cell - 1 + other, 94)
    row = self.row + row_inc
    if row > 94:
      raise OverflowError("RowCell %s + %d overflow" % (self, other))
    return RowCell(row, cell_rem + 1)

  def __sub__(self, other):
    """Return the linear difference between two row-cell pairs.
    Inverse of __add__().

    Args:
      other: Another RowCell instance.

    Returns:
      An integer with the linear difference between the two row-cell pairs.
    """
    row_diff = self.row - other.row
    cell_diff = self.cell - other.cell
    return row_diff * 94 + cell_diff

  def ToDecimalString(self):
    """Create a 4-decimal-digit string from the row-cell values.

    >>> str(RowCell(1, 94))
    '0194'

    Returns: The 4-decimal-digit string.
    """
    return "%02d%02d" % (self.row, self.cell)

  def To2022(self):
    """Convert the row-cell values to an ISO-2022 "GL" byte pair.

    Returns:
      The pair of ISO-2022 "GL" bytes corresponding to the row-cell value pair.
    """
    return (self.row + 0x20, self.cell + 0x20)

  def ToShiftJis(self):
    """Convert the row-cell values to Shift-JIS.

    Returns:
      The pair of Shift-JIS bytes corresponding to the row-cell value pair.
    """
    b1 = self.row
    b2 = self.cell
    if b1 & 1:
      b1 += 1
      if b2 <= 0x3f:
        b2 += 0x3f
      else:
        b2 += 0x40
    else:
      b2 += 0x9e;
    b1 >>= 1
    if b1 <= 0x1f:
      b1 += 0x80
    else:
      b1 += 0xc0
    return (b1, b2)

  def ToShiftJisString(self):
    """Convert the row-cell values to Shift-JIS in a hex-digit string.

    Returns:
      The pair of Shift-JIS bytes corresponding to the row-cell value pair,
      with the Shift-JIS bytes represented as 2 uppercase hex digits each.
    """
    sjis = self.ToShiftJis()
    return "%02X%02X" % (sjis[0], sjis[1])


def FromHexString(s):
  """Create a RowCell instance from a 4-hex-digit string.

  Parses the 4-hex-digit string into a pair of bytes and instantiates a RowCell.
  >>> str(FromHexString('015E'))
  '015E'

  Returns:
    A RowCell instance with the row-cell value pair.

  Raises:
    ValueError: The string does not contain exactly 4 hex digits or
      one or both values are not 1..0x5e.
  """
  if len(s) != 4: raise ValueError("the string must contain 4 hex digits")
  return RowCell(int(s[0:2], 16), int(s[2:4], 16))


def FromDecimalString(s):
  """Create a RowCell instance from a 4-decimal-digit string.

  Parses the 4-decimal-digit string into a pair of bytes and instantiates
  a RowCell.
  >>> str(FromHexString('0194'))
  '015E'

  Returns:
    A RowCell instance with the row-cell value pair.

  Raises:
    ValueError: The string does not contain exactly 4 decimal digits or
      one or both values are not 1..94.
  """
  if len(s) != 4: raise ValueError("the string must contain 4 decimal digits")
  return RowCell(int(s[0:2], 10), int(s[2:4], 10))


def From2022(b1, b2):
  """Create a RowCell instance from an ISO-2022 "GL" byte pair.

  Returns:
    A RowCell instance with the row-cell value pair.

  Raises:
    ValueError: One or both values are not 0x21..0x7e.
  """
  if not 0x21 <= b1 <= 0x7e or not 0x21 <= b2 <= 0x7e:
    raise ValueError("value out of range")
  return RowCell(b1 - 0x20, b2 - 0x20)


def FromShiftJis(b1, b2):
  """Create a RowCell instance from a Shift-JIS byte pair.

  Returns:
    A RowCell instance with the row-cell value pair.

  Raises:
    ValueError: The lead byte is not 0x81..0x9f or 0xe0..0xef, and/or
      the trail byte is not 0x40..0x7e or 0x80..0xfc.
  """
  if not ((0x81 <= b1 <= 0x9f or 0xe0 <= b1 <= 0xef) and
          0x40 <= b2 <= 0xfc and b2 != 0x7f):
    raise ValueError("value out of range")
  if b1 <= 0x9f:
    b1 = (b1 - 0x80) << 1
  else:
    b1 = (b1 - 0xc0) << 1
  if b2 <= 0x9e:
    b1 -= 1
    if b2 <= 0x7e:
      b2 -= 0x3f
    else:
      b2 -= 0x40
  else:
    b2 -= 0x9e
  return RowCell(b1, b2)


def FromShiftJisString(s):
  """Create a RowCell instance from a 4-hex-digit Shift-JIS string.

  Parses the 4-hex-digit Shift-JIS string into a pair of bytes and instantiates
  a RowCell.
  >>> str(FromHexString('8140'))
  '0101'

  Returns:
    A RowCell instance with the row-cell value pair.

  Raises:
    ValueError: The string does not contain exactly 4 hex digits or
      does not contain a Shift-JIS (JIS X 0208) code.
  """
  if len(s) != 4: raise ValueError("the string must contain 4 hex digits")
  return FromShiftJis(int(s[0:2], 16), int(s[2:4], 16))
