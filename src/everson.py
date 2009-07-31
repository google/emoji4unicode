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
  doc: WG2 document number string, e.g., "N3607".
  id_to_everson_uni: Maps Emoji symbol IDs to Unicode code points
      proposed by Everson & Stoetzner.
  id_to_glyph_change: Maps Emoji symbol IDs to 1/0/-1/-2 for
      good/neutral/bad/really bad glyph changes.
  id_to_name_change: Maps Emoji symbol IDs to 1/0/-1 for good/neutral/bad
      name changes.
"""

__author__ = "Markus Scherer"

import nameslist
import os.path

doc = "N3607"

id_to_everson_uni = {}

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
    "7DC": 1,
    # other symbols
    "005": 1, "01B": 1, "038": 1,
    "4B0": 1, "4B1": 1, "4BF": 1,
    "7EE": 1,
    # *** neutral
    # sports
    "7D8": 0, "7D9": 0, "7DA": 0, "7DE": 0,
    "7EB": 0, "7EC": 0, "7ED": 0, "7EF": 0,
    # other symbols
    "00D": 0, "016": 0, "190": 0, "19F": 0, "1A0": 0, "1AE": 0, "1B1": 0,
    "4B2": 0, "4B3": 0, "4B4": 0, "4B6": 0, "4B7": 0, "4B8": 0, "4B9": 0,
    "4BA": 0, "4C0": 0, "4CA": 0,
    "4D6": 0, "4D8": 0, "4DD": 0, "4E3": 0, "4F2": 0, "4F6": 0,
    "506": 0, "509": 0, "550": 0,
    "7DF": 0, "7E0": 0, "7E4": 0, "7E5": 0, "7E6": 0, "7E7": 0, "7E8": 0,
    "7F1": 0, "7F2": 0, "7F3": 0,
    "802": 0, "803": 0, "812": 0, "821": 0,
    "980": 0, "982": 0,
    "B33": 0, "B34": 0, "B5A": 0,
    "B82": 0, "B85": 0, "B86": 0, "B87": 0, "B8A": 0, "B8D": 0, "B8F": 0,
    "B90": 0,
    # *** somewhat bad
    # animals
    "1B9": -1, "1BA": -1, "1BB": -1, "1BD": -1, "1BE": -1, "1C8": -1, "1C9": -1,
    "1CC": -1, "1CE": -1, "1D3": -1, "1D4": -1, "1D5": -1, "1D6": -1, "1D9": -1,
    "1DC": -1,
    # other symbols
    "507": -1,
    # *** really bad
    # animals
    "1B7": -2, "1B8": -2, "1BF": -2, "1C0": -2, "1C1": -2, "1C2": -2, "1C3": -2,
    "1C5": -2, "1C7": -2, "1CA": -2, "1CD": -2, "1CF": -2, "1D0": -2, "1D1": -2,
    "1D2": -2, "1D7": -2, "1DF": -2,
    # other symbols
    "039": -2, "044": -2, "198": -2, "1B2": -2, "02A": -2, "4B5": -2, "4BD": -2,
    "4C4": -2, "4DE": -2, "4FC": -2, "505": -2, "513": -2, "7D5": -2, "7E2": -2,
    "7E3": -2, "7F4": -2, "801": -2, "809": -2
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
    "B1E": 0, "B1F": 0, "B42": 0, "B85": 0, "B8E": 0, "B92": 0,
    # *** bad
    # landmarks
    "4C4": -1, "4C6": -1, "4C7": -1, "4C8": -1,
    # other symbols
    "012": -1, "013": -1, "016": -1,
    "039": -1, "03C": -1, "042": -1, "046": -1, "048": -1, "04D": -1,
    "1A4": -1, "1B2": -1, "1E2": -1, "1CB": -1, "1D6": -1,
    "4B1": -1, "4C3": -1, "4CD": -1, "4F4": -1, "4FB": -1,
    "506": -1, "50D": -1, "513": -1,
    "7DF": -1, "7E0": -1, "7E4": -1, "7E6": -1, "7EF": -1, "7F4": -1, "7F9": -1,
    "80C": -1, "821": -1,
    "965": -1, "968": -1, "96D": -1,
    "B33": -1, "B34": -1, "B91": -1
}

def Load():
  """Parse ../data/everson/ files."""
  # TODO(mscherer): Add argument for root data folder path.
  global id_to_everson_uni
  if id_to_everson_uni: return  # Already loaded.
  here = os.path.dirname(__file__)
  data_path = os.path.join(here, "..", "data")
  _ParseMapping(data_path)
  _ParseNamesList(data_path)


def GetUnicode(id):
  """Get the Everson/Stoetzner code point.

  Args:
    id: Emoji symbol ID

  Returns:
    The Everson/Stoetzner code point.
  """
  return id_to_everson_uni.get(id)


def GetName(id):
  """Get the Everson/Stoetzner character name.

  Args:
    id: Emoji symbol ID

  Returns:
    The Everson/Stoetzner character name.
  """
  everson_uni = id_to_everson_uni[id]
  return _symbol_data[everson_uni][0]


def GetAnnotations(id):
  """Get the Everson/Stoetzner character annotations.

  Args:
    id: Emoji symbol ID

  Returns:
    The Everson/Stoetzner character annotations (list of strings).
  """
  everson_uni = id_to_everson_uni[id]
  return _symbol_data[everson_uni][1]


def GetGoodGlyphChanges(id_to_symbol):
  return _FilterSymbols(id_to_symbol, id_to_glyph_change, lambda x: x > 0)


def GetNeutralGlyphChanges(id_to_symbol):
  return _FilterSymbols(id_to_symbol, id_to_glyph_change, lambda x: x == 0)


def GetSomewhatBadGlyphChanges(id_to_symbol):
  return _FilterSymbols(id_to_symbol, id_to_glyph_change, lambda x: x == -1)


def GetBadGlyphChanges(id_to_symbol):
  return _FilterSymbols(id_to_symbol, id_to_glyph_change, lambda x: x == -2)


def GetGoodNameChanges(id_to_symbol):
  return _FilterSymbols(id_to_symbol, id_to_name_change, lambda x: x > 0)


def GetNeutralNameChanges(id_to_symbol):
  return _FilterSymbols(id_to_symbol, id_to_name_change, lambda x: x == 0)


def GetBadNameChanges(id_to_symbol):
  return _FilterSymbols(id_to_symbol, id_to_name_change, lambda x: x < 0)


def _FilterSymbols(id_to_symbol, id_to_change, filter_fn):
  symbols = [(int(id_to_symbol[id].GetProposedUnicode(), 16), id_to_symbol[id])
             for id in id_to_change.keys()
             if filter_fn(id_to_change[id])]
  symbols.sort()  # Sort by UTC-proposed Unicode code point.
  symbols = [pair[1] for pair in symbols]  # Remove code points.
  return symbols


def _ParseMapping(data_path):
  global id_to_everson_uni
  filename = os.path.join(data_path, "everson", "n3607-emoji-mapping.txt")
  file = open(filename, "r")
  for line in file:
    line = line.rstrip()  # Remove trailing newlines etc.
    index = line.find("#")  # Remove comments.
    if index >= 0: line = line[:index].rstrip()
    if not line: continue  # Skip empty lines.
    if line.startswith("-"): continue  # Skip new characters.
    id, everson_uni = line.split()
    id_to_everson_uni[id] = everson_uni


def _ParseNamesList(data_path):
  global _symbol_data
  _symbol_data = {}

  # Read the NamesList.txt-format file.
  filename = os.path.join(data_path, "everson", "n3607-emoji.lst")
  for record in nameslist.Read(filename):
    if "uni" in record:
      uni = record["uni"]
      if "data" in record:
        ann = record["data"]
      else:
        ann = []
      _symbol_data[uni] = (record["name"], ann)
