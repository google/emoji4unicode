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

"""Parse and represent symbols data from Everson & Stoetzner.

Attributes:
  proposed_uni_to_everson: Maps UTC-proposed Unicode code points to ones
      proposed by Everson & Stoetzner.
  id_to_glyph_change: Maps Emoji symbol IDs to 1/0/-1/-2 for
      good/neutral/bad/really bad glyph changes.
  id_to_name_change: Maps Emoji symbol IDs to 1/0/-1 for good/neutral/bad
      name changes.
"""

__author__ = "Markus Scherer"

import codecs
import os.path
import re

proposed_uni_to_everson = {}

id_to_glyph_change = {
    # *** improvements
    # faces/emoticons
    "320": 1, "321": 1, "322": 1, "323": 1, "324": 1, "325": 1, "326": 1,
    "327": 1, "328": 1, "329": 1, "32A": 1, "32B": 1, "32C": 1, "32D": 1,
    "32E": 1, "32F": 1, "330": 1, "331": 1, "332": 1, "333": 1, "334": 1,
    "335": 1, "338": 1, "339": 1, "33A": 1, "33B": 1, "33C": 1, "33D": 1,
    "33E": 1, "33F": 1, "340": 1, "341": 1, "342": 1, "343": 1, "344": 1,
    "345": 1, "346": 1, "347": 1, "348": 1, "349": 1, "34A": 1, "34B": 1,
    "34C": 1, "34D": 1, "34E": 1, "34F": 1, "350": 1,
    # sports
    "7D8": 1, "7D9": 1, "7DA": 1, "7DC": 1, "7DE": 1,
    # other symbols
    "005": 1, "01B": 1, "038": 1, "19F": 1, "1A0": 1, "4B0": 1, "4B1": 1,
    "4BF": 1, "4C0": 1,
    "7E8": 1, "7EC": 1, "7EE": 1, "7EF": 1, "7F1": 1, "7F2": 1, "7F3": 1,
    "809": 1,
    # *** neutral
    "00D": 0, "016": 0, "1AE": 0, "1B1": 0,
    "4B2": 0, "4B3": 0, "4B4": 0, "4B6": 0, "4B7": 0, "4B8": 0, "4B9": 0,
    "4BA": 0, "4CA": 0, "4DD": 0, "4E3": 0, "4F2": 0,
    "506": 0,
    "7DF": 0, "7E0": 0, "7E4": 0, "7E6": 0,
    "802": 0, "803": 0, "812": 0,
    "980": 0, "982": 0,
    "B33": 0, "B34": 0,
    "B82": 0, "B85": 0, "B86": 0, "B87": 0, "B8A": 0, "B8D": 0, "B8F": 0,
    "B90": 0
}

id_to_name_change = {
    # *** improvements
    "1AF": 1, "7F0": 1, "B46": 1,
    # *** neutral
    "006": 0, "011": 0, "015": 0, "04A": 0, "056": 0,
    "19A": 0,
    "4B3": 0, "4CE": 0, "4E2": 0, "4E3": 0,
    "532": 0,
    "7F7": 0, "7F8": 0,
    "802": 0, "812": 0, "81C": 0, "820": 0, "838": 0, "83A": 0,
    "975": 0, "978": 0,
    "B1E": 0, "B1F": 0, "B42": 0, "B85": 0, "B8E": 0, "B92": 0
}

def Load():
  """Parse ../data/everson/ files."""
  # TODO(mscherer): Add argument for root data folder path.
  global proposed_uni_to_everson
  if proposed_uni_to_everson: return  # Already loaded.
  here = os.path.dirname(__file__)
  data_path = os.path.join(here, "..", "data")
  _ParseMapping(data_path)
  _ParseNamesList(data_path)

def GetUnicode(uni):
  """Get the Everson/Stoetzner code point.

  Args:
    uni: emoji4unicode-proposed code point

  Returns:
    The Everson/Stoetzner code point.
  """
  return proposed_uni_to_everson.get(uni)

def GetName(uni):
  """Get the Everson/Stoetzner character name.

  Args:
    uni: emoji4unicode-proposed code point

  Returns:
    The Everson/Stoetzner character name.
  """
  everson_uni = proposed_uni_to_everson[uni]
  return _symbol_data[everson_uni][0]

def GetAnnotations(uni):
  """Get the Everson/Stoetzner character annotations.

  Args:
    uni: emoji4unicode-proposed code point

  Returns:
    The Everson/Stoetzner character annotations (list of strings).
  """
  everson_uni = proposed_uni_to_everson[uni]
  return _symbol_data[everson_uni][1]

def _ParseMapping(data_path):
  global proposed_uni_to_everson
  filename = os.path.join(data_path, "everson", "n3607-emoji-mapping.txt")
  file = open(filename, "r")
  for line in file:
    line = line.strip()  # Remove trailing newlines etc.
    index = line.find("#")  # Remove comments.
    if index >= 0: line = line[:index].rstrip()
    if not line: continue  # Skip empty lines.
    if line.startswith("-"): continue  # Skip new characters.
    uni, everson_uni = line.split()
    proposed_uni_to_everson[uni] = everson_uni

# TODO(markus): Create a reusable NamesList.txt parsing library.
# See nameslist_to_unicodedata.py.
def _ParseNamesList(data_path):
  # Match a NAME_LINE in the Unicode NamesList.txt file.
  name_line_re = re.compile(r"^([0-9A-F]{4,6})\t(.+)$")

  global _symbol_data
  _symbol_data = {}

  # Read the NamesList.txt-format file.
  filename = os.path.join(data_path, "everson", "n3607-emoji.lst")
  in_file = codecs.open(filename, "r", "ISO-8859-1")
  uni = ""  # Unicode code point
  ann = []  # annotations
  for line in in_file:
    comment_start = line.find(";")
    if comment_start >= 0:
      line = line[:comment_start].rstrip()  # Remove comment.
    else:
      line = line.rstrip()  # Remove line ending.
    if not line:
      # Skip EMPTY_LINE or FILE_COMMENT.
      continue
    if uni:
      # Most CHAR_ENTRY data lines for a character start with a TAB.
      if line.startswith("\t"):
        ann.append(line[1:])
        continue
      elif line.startswith("@+\t"):
        # A NOTICE_LINE which is part of the current CHAR_ENTRY.
        continue
      else:
        # If a line does not start with a TAB and is not a NOTICE_LINE,
        # then it indicates the end of a CHAR_ENTRY.
        _symbol_data[uni] = (name, ann)
        uni = ""
        ann = []
    match = name_line_re.match(line)
    if match:
      # Begin a new CHAR_ENTRY.
      uni = match.group(1)
      name = match.group(2)
      ann = []

  if uni:
    # Print data for the last CHAR_ENTRY.
    _symbol_data[uni] = (name, ann)
