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

We do not use the Python unicodedata module because

1. The unicodedata module uses at best data from the latest Unicode version,
and at worst data from several years ago, depending on the age of the Python
distribution. (The online Python 2.5 documentation says it's Unicode 4.1,
which is from March 2005.)

For this project, we need to use the very latest data available, including characters that will go into future releases.

Even the initial data used in this project only includes AMD 5 characters,
and we need AMD 6 with recent modifications to include the
accepted ARIB symbols. ("AMD" means ISO 10646 Amendment.)

2. The unicodedata module documentation is not clear. It says the lookup()
function returns a "Unicode character". What does that mean for supplementary
characters on a Python installation with default 16-bit Unicode strings, like
on Windows and the Mac? Will it return a surrogate pair or throw an exception?

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
