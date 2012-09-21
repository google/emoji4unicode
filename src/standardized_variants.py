#!/usr/bin/python2.6
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

"""Load and make available Unicode Standardized Variants data."""

__author__ = "Markus Scherer"

import os.path

# Code points with Emoji variation selector sequences.
_emoji_vs_code_points = set()

def Load():
  """Loads Unicode Standardized Variants data."""
  # TODO(mscherer): Add argument for root data folder path.
  filename = os.path.join(os.path.dirname(__file__),
                          "..", "data", "unicode", "StandardizedVariants.txt")
  file = open(filename, "r")
  for line in file:
    line = line.strip()  # Remove trailing newlines etc.
    index = line.find("#")  # Remove comments.
    if index >= 0: line = line[:index].rstrip()
    if not line: continue  # Skip empty lines.
    fields = line.split(";")
    # Sample lines:
    # 2601 FE0E; text style;  # CLOUD
    # 2601 FE0F; emoji style; # CLOUD
    description = fields[1]
    if "emoji style" not in description: continue  # Ignore non-Emoji sequences.
    # Turn the Unicode code point sequence string into an integer list.
    code_points = fields[0].split()
    for i in range(len(code_points)):
      code_points[i] = int(code_points[i], 16)
    if code_points[-1] != 0xFE0F:
      # The sequence must end with Variation Selector 16.
      raise ValueError("emoji style for sequence without VS16: " + line)
    if len(code_points) != 2:
      raise ValueError("current limitation: emoji style sequences must be " +
                       "one code point plus VS16")
    _emoji_vs_code_points.add(code_points[0])


def GetSetOfUnicodeWithEmojiVS():
  return _emoji_vs_code_points
