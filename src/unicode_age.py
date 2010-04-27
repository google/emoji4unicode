#!/usr/bin/python2.4
#
# Copyright 2010 Google Inc.
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

"""Load and make available Unicode code point Age data."""

__author__ = "Markus Scherer"

import os.path

_ranges_to_age = []

def Load():
  """Loads Unicode character Age data."""
  # TODO(mscherer): Add argument for root data folder path.
  filename = os.path.join(os.path.dirname(__file__),
                          "..", "data", "unicode", "DerivedAge.txt")
  file = open(filename, "r")
  for line in file:
    line = line.strip()  # Remove trailing newlines etc.
    index = line.find("#")  # Remove comments.
    if index >= 0: line = line[:index].rstrip()
    if not line: continue  # Skip empty lines.
    fields = line.split(";")
    range = fields[0].split("..")
    start = int(range[0], 16)
    if len(range) == 1:
      end = start
    else:
      end = int(range[1], 16)
    _ranges_to_age.append((start, end, fields[1].lstrip()))
  _ranges_to_age.sort()


def _FindAge(uni):
  """Returns the age string of a single code point integer."""
  # binary search
  start = 0
  limit = len(_ranges_to_age)
  while start < limit:
    i = (start + limit) / 2
    tuple = _ranges_to_age[i]
    if uni < tuple[0]:
      limit = i
    elif uni > tuple[1]:
      start = i + 1
    else:
      return tuple[2]
  return None


def GetAge(uni):
  """Returns age string for newest character in
  plus-separated input code point string,
  or empty string if all code points are unassigned.
  """
  age = u""
  for code_point in uni.split('+'):
    if code_point:
      cp_age = _FindAge(int(code_point, 16))
      if cp_age and cp_age > age: age = cp_age
  return age
