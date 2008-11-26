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

"""Load and make available Unicode character names data.

This module does not currently handle algorithmic names (for Han and Hangul
characters) nor registered names of sequences.

Attributes:
  code_points_to_names: Map from code points to character names.
  names_to_code_points: Map from character names to code points.
"""

__author__ = "Markus Scherer"

import os.path

code_points_to_names = {}
names_to_code_points = {}

def Load():
  """Load Unicode character names data."""
  # TODO(mscherer): Add argument for root data folder path.
  filename = os.path.join(os.path.dirname(__file__),
                          "..", "data", "unicode", "UnicodeData.txt")
  file = open(filename, "r")
  for line in file:
    line = line.strip()  # Remove trailing newlines etc.
    index = line.find("#")  # Remove comments.
    if index >= 0: line = line[:index].rstrip()
    if not line: continue  # Skip empty lines.
    fields = line.split(";")
    code_point = fields[0]
    name = fields[1]
    if name.startswith("<"): continue
    code_points_to_names[code_point] = name
    names_to_code_points[name] = code_point
