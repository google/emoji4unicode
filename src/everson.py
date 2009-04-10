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

"""Parse and represent symbols data from Everson & Stoetzner."""

__author__ = "Markus Scherer"

import codecs
import os.path
import re

to_everson = {}

def Load():
  """Parse ../data/everson/ files."""
  # TODO(mscherer): Add argument for root data folder path.
  global to_everson
  global _symbol_data
  if to_everson: return  # Already loaded.
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
  return to_everson.get(uni)

def GetName(uni):
  """Get the Everson/Stoetzner character name.

  Args:
    uni: emoji4unicode-proposed code point

  Returns:
    The Everson/Stoetzner character name.
  """
  everson_uni = to_everson[uni]
  return _symbol_data[everson_uni][0]

def GetAnnotations(uni):
  """Get the Everson/Stoetzner character annotations.

  Args:
    uni: emoji4unicode-proposed code point

  Returns:
    The Everson/Stoetzner character annotations (list of strings).
  """
  everson_uni = to_everson[uni]
  return _symbol_data[everson_uni][1]

def _ParseMapping(data_path):
  global to_everson
  filename = os.path.join(data_path, "everson", "n3607-emoji-mapping.txt")
  file = open(filename, "r")
  for line in file:
    line = line.strip()  # Remove trailing newlines etc.
    index = line.find("#")  # Remove comments.
    if index >= 0: line = line[:index].rstrip()
    if not line: continue  # Skip empty lines.
    if line.startswith("-"): continue  # Skip new characters.
    uni, everson_uni = line.split()
    to_everson[uni] = everson_uni

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
