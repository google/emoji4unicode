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

import nameslist

# Read the NamesList.txt-format file with AMD6 characters
# and print data in the UnicodeData.txt format.
for record in nameslist.Read("uc52-a-FPDAM6-HongKong.lst"):
  if "uni" in record:
    print "%s;%s;;;;%s;;;;N;;;;;" % (
        record["uni"], record["name"], nameslist.GetDecomposition(record))
