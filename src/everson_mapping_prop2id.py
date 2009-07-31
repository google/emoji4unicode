#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
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

"""Parse n3607-emoji-mapping.txt and change proposed code points to IDs.

Proposed Emoji code points change over time. In order to avoid having to
update the mapping data each time the proposed code points change,
change it just once and use the stable Emoji symbol IDs instead.
"""

__author__ = "Markus Scherer"

import emoji4unicode
import os.path

emoji4unicode.Load()
sorted_uni_symbols = emoji4unicode.GetSymbolsInProposalSortedByUnicode()
uni_to_id = {}
for uni_symbol in sorted_uni_symbols:
  uni_ints = uni_symbol[0]
  if len(uni_ints) == 1:
    uni = "%04X" % uni_ints[0]
    uni_to_id[uni] = uni_symbol[1].id

here = os.path.dirname(__file__)
data_path = os.path.join(here, "..", "data")
filename = os.path.join(data_path, "everson", "n3607-emoji-mapping.txt")
file = open(filename, "r")
for orig_line in file:
  orig_line = orig_line.rstrip()  # Remove trailing newlines etc.
  index = orig_line.find("#")  # Remove comments.
  if index >= 0:
    line = orig_line[:index].rstrip()
  else:
    line = orig_line
  if not line or line.startswith("-"):  # Skip empty lines and new characters.
    print orig_line
    continue
  uni, everson_uni = line.split()
  print "%s\t%s" % (uni_to_id[uni], everson_uni)
