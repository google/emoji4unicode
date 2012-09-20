#!/usr/bin/python2.4
#
# Copyright 2012 Google Inc.
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

"""Print useful sets of Unicode code points."""

__author__ = "Markus Scherer"

import emoji4unicode
import standardized_variants

def _EscapeForCpp(c):
  """Returns a C++ escape sequence for the code point."""
  if c <= 0xffff:
    return "\\u%04x" % c
  else:
    return "\\U%08x" % c


def _EscapeForJava(c):
  """Returns a Java escape sequence for the code point."""
  if c <= 0xffff:
    return "\\u%04x" % c
  else:
    # Emit two \uhhhh sequences, one for each surrogate.
    # Java does not have a \Uhhhhhhhh escape sequence that would support
    # supplementary code points directly.
    lead = 0xd7c0 + (c >> 10)
    trail = 0xdc00 + (c & 0x3ff)
    return "\\u%04x\\u%04x" % (lead, trail)


def _SetToRanges(s):
  code_points = sorted(s)
  code_points.append(0x110000)  # terminator
  ranges = []
  # Start the first range.
  start = code_points[0]
  prev = start
  for c in code_points[1:]:
    if c == (prev + 1):
      # Continue the current range.
      prev += 1
    else:
      # Finish the current range, start a new one.
      ranges.append((start, prev))
      start = c
      prev = c
  return ranges


def SetToUnicodeSetPattern(s, escape):
  """Turns the set s of code points into a UnicodeSet pattern.
  Creates ranges, like in a regex character class."""
  ranges = _SetToRanges(s)
  pattern = "["
  for (start, end) in ranges:
    if start == end:
      pattern += escape(start)
    elif (start + 1) == end:
      pattern += escape(start) + escape(end)
    else:
      pattern += escape(start) + "-" + escape(end)
  pattern += "]"
  return pattern


def main():
  standardized_variants.Load()
  emoji_vs_code_points = standardized_variants.GetSetOfUnicodeWithEmojiVS()
  print
  print ("Unicode Standard code points with emoji-style " +
      "Variation Selector sequences:")
  print
  print "C++: " + SetToUnicodeSetPattern(emoji_vs_code_points, _EscapeForCpp)
  print
  print "Java: " + SetToUnicodeSetPattern(emoji_vs_code_points, _EscapeForJava)

  emoji4unicode.Load()
  pua_vs_code_points = set()
  for symbol in emoji4unicode.GetSymbols():
    # Get the symbol's standard Unicode code point or sequence.
    uni = symbol.GetUnicode()
    if not uni: continue
    first = int(uni.split("+")[0], 16)  # The symbol's first Unicode code point.
    if first not in emoji_vs_code_points: continue
    # Get the Google Private Use Area code point.
    pua = symbol.GetCarrierUnicode("google")
    if not pua.startswith("<"):
      # Round-trip, must be a single code point.
      pua_vs_code_points.add(int(pua, 16))
  print
  print ("Google PUA code points corresponding to Unicode Standard " +
      "code points with emoji-style Variation Selector sequences:")
  print
  print "C++: " + SetToUnicodeSetPattern(pua_vs_code_points, _EscapeForCpp)
  print
  print "Java: " + SetToUnicodeSetPattern(pua_vs_code_points, _EscapeForJava)

  if len(emoji_vs_code_points) != len(pua_vs_code_points):
    raise ValueError("Mismatch: %d standard code points with VS16 but " +
        "%d corresponding Google PUA code points" %
        (len(emoji_vs_code_points), len(pua_vs_code_points)))

if __name__ == "__main__":
  main()
