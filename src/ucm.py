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

"""Parse and represent a .ucm Unicode conversion mapping file.

See the ICU User Guide chapter "Conversion Data" for details:
http://icu-project.org/userguide/conversion-data.html

This module performs simplified parsing, without much validity checking.
It assumes well-formed .ucm files.
"""

__author__ = "Markus Scherer"

class UCMFile(object):
  """Parse and represent a .ucm Unicode conversion mapping file.

  Attributes:
    round_trip_code_points: Code points with round-trip mappings.
         Stored as a frozenset of 4..6-hex-digit strings.
         Sequences like "0061+0308" are possible.
    from_unicode: Mapping (dictionary) from Unicode code points (or sequences)
        to charset bytes. Maps from strings (as in the round-trip set)
        to strings.
  """
  def __init__(self, filename):
    """Parse a .ucm file.

    Args:
      filename: Path/filename of the .ucm file.
    """
    self.round_trip_code_points = set()
    self.from_unicode = {}
    file = open(filename, "r")
    for line in file:
      line = line.strip()  # Remove trailing newlines etc.
      index = line.find("#")  # Remove comments.
      if index >= 0: line = line[:index].rstrip()
      if not line: continue  # Skip empty lines.
      if line.startswith("<U"):
        uni, bytes, precision = line.split()
        uni = _RemoveMappingSyntax(uni)
        bytes = _RemoveMappingSyntax(bytes)
        if precision == "|0":
          self.round_trip_code_points.add(uni)
        if precision == "|0" or precision == "|1":
          self.from_unicode[uni] = bytes
    self.round_trip_code_points = frozenset(self.round_trip_code_points)


_MAPPING_CHARS = frozenset("0123456789ABCDEF+")

def _RemoveMappingSyntax(s):
  result = ""
  for c in s:
    if c in _MAPPING_CHARS: result += c
  return result
