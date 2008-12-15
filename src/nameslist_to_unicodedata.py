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

"""Extract Unicode character data from a NamesList.txt-format file.

Print corresponding data lines in UnicodeData.txt file format.
"""

__author__ = "Markus Scherer"

import codecs
import os.path
import re

# Match a NAME_LINE in the Unicode NamesList.txt file.
name_line_re = re.compile(r"^([0-9A-F]{4,6})\t(.+)$")

# Match a DECOMPOSITION in the Unicode NamesList.txt file.
decomp_line_re = re.compile(r"^\t(:|#) (.+)$")

# Read the NamesList.txt-format file with AMD6 characters
# and print data in the UnicodeData.txt format.
in_file = codecs.open("uc52-a-FPDAM6-HongKong.lst", "r", "ISO-8859-1")
uni = ""
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
      match = decomp_line_re.match(line)
      if match:
        decomp = match.group(2)
        if line.find("#") >= 0 and line.find("<") < 0:
          decomp = "<compat> " + decomp
      continue
    elif line.startswith("@+\t"):
      # A NOTICE_LINE which is part of the current CHAR_ENTRY.
      continue
    else:
      # If a line does not start with a TAB and is not a NOTICE_LINE,
      # then it indicates the end of a CHAR_ENTRY.
      print "%s;%s;;;;%s;;;;N;;;;;" % (uni, name, decomp)
      uni = ""
  match = name_line_re.match(line)
  if match:
    # Begin a new CHAR_ENTRY.
    uni = match.group(1)
    name = match.group(2)
    decomp = ""

if uni:
  # Print data for the last CHAR_ENTRY.
  print "%s;%s;;;;%s;;;;N;;;;;" % (uni, name, decomp)
