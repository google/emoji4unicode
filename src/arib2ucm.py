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

"""Convert the ARIB Unicode mappings into .ucm mapping syntax.

This script reads mapping lines from ../data/arib/arib.txt and reformats them
into roundtrip mappings in ICU's .ucm conversion mapping file format.
It changes the decimal row-cell ARIB values into Shift-JIS codes.
Output goes to stdout.

The file needs manual post-processing to fix precision indicators for
reverse fallbacks and to add headers and comments.
"""

__author__ = "Markus Scherer"

import row_cell

def main():
  arib_file = open("../data/arib/arib.txt", "r")
  for line in arib_file:
    line = line.strip()  # Remove trailing newlines etc.

    index = line.find("#")  # Remove comments.
    if index >= 0: line = line[:index].rstrip()

    # Skip empty lines and lines that contain only comments.
    if not line: continue

    arib, uni = line.split()
    sjis = row_cell.FromDecimalString(arib).ToShiftJisString()
    print "<U%s> \\x%s\\x%s |0  # ARIB-%s" % (uni, sjis[0:2], sjis[2:4], arib)
  arib_file.close()

if __name__ == "__main__":
  main()
