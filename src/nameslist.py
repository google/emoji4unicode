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

"""Parse a Unicode NamesList.txt-format file.

The file format is documented in
http://www.unicode.org/Public/UNIDATA/NamesList.html
"""

__author__ = "Markus Scherer"

import codecs
import re

def Read(filename):
  """Reads data records from a Unicode NamesList.txt-format file.

  Args:
    filename: Path and filename for the NamesList.txt-format file to read.

  Yields:
    A record per character. Each record is a Python dictionary.
    For each character in the NamesList,
    the "uni" key has the code point as a 4-6-hex-digit string,
    the "name" key has the character name,
    and the "data" key has a list of strings which are the lines of data
    for this character, minus the leading TAB.
  """
  # Match a NAME_LINE in the Unicode NamesList.txt file.
  name_line_re = re.compile(r"^([0-9A-F]{4,6})\t(.+)$")
  # NamesList.txt is in "ISO-8859-1" up to Unicode 6.1,
  # and in "UTF-8" starting with Unicode 6.2.
  in_file = codecs.open(filename, "r", "UTF-8")
  # A record is a unit of data we yield to the caller.
  # Normally, it contains the data for one character.
  record = {}
  for line in in_file:
    comment_start = line.find(";")
    if comment_start >= 0:
      if line.startswith(";\t= e-"):
        # Starting 2009-nov-04 the NamesList has commented-out Emoji ID lines
        # so that the Emoji ID do not show up in UniBook chart production.
        line = line[1:].rstrip()  # Remove the ; and the line ending.
      else:
        line = line[:comment_start].rstrip()  # Remove comment.
    else:
      line = line.rstrip()  # Remove line ending.
    if not line:
      # Skip EMPTY_LINE or FILE_COMMENT.
      continue
    if "uni" in record:
      # Most CHAR_ENTRY data lines for a character start with a TAB.
      if line.startswith("\t"):
        if "data" not in record:
          record["data"] = []
        record["data"].append(line[1:])
        continue
      elif line.startswith("@+\t"):
        # A NOTICE_LINE which is part of the current CHAR_ENTRY.
        continue
      else:
        # If a line does not start with a TAB and is not a NOTICE_LINE,
        # then it indicates the end of a CHAR_ENTRY.
        yield record
        record = {}
    match = name_line_re.match(line)
    if match:
      # Begin a new CHAR_ENTRY.
      record["uni"] = match.group(1)
      record["name"] = match.group(2)

  if record:
    # The last data record in the file.
    yield record


_emoji_alias_re = re.compile(r"^= e-([0-9A-F]{3})$")

def GetEmojiID(record):
  """Gets the Emoji ID from a CHAR_ENTRY record.

  During development of Unicode 6.0/ISO 10646 AMD8,
  each Emoji symbol in the NamesList temporarily has an additional alias line
  with its Emoji symbol ID.

  Returns:
    The Emoji symbol ID as a 3-hex-digit string, if present.
    Otherwise None.
  """
  if "uni" in record and "data" in record:
    data = record["data"]
    for item in data:
      match = _emoji_alias_re.match(item)
      if match:
        return match.group(1)
  return None


# Match a DECOMPOSITION in the Unicode NamesList.txt file.
_decomp_re = re.compile(r"^(:|#) (.+)$")

def GetDecomposition(record):
  """Gets the decomposition mapping from a CHAR_ENTRY record.

  Returns:
    The decomposition mapping string, if the character decomposes.
    Compatibility decompositions begin with <compat>, <wide> etc.
    Returns an empty string if the character does not decompose.
  """
  if "uni" in record and "data" in record:
    data = record["data"]
    for item in data:
      match = _decomp_re.match(item)
      if match:
        decomp = match.group(2)
        if match.group(1) == "#" and not decomp.startswith("<"):
          decomp = "<compat> " + decomp
        return decomp
  return ""
