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

"""Update emoji4unicode.xml: Remove oldname attributes.

Intended for cleanup before using update_e4u_from_nameslist.py
so that the diffs for that are smaller.
This script reads emoji4unicode.xml, removes the oldname attributes,
and writes a modified XML file to ../generated/emoji4unicode.xml.
"""

__author__ = "Markus Scherer"

import os.path
import xml.dom.minidom
import emoji4unicode
import nameslist

def main():
  here = os.path.dirname(__file__)
  e4u_filename = os.path.join(here, "..", "data", "emoji4unicode.xml")
  doc = xml.dom.minidom.parse(e4u_filename)
  root = doc.documentElement
  for symbol in root.getElementsByTagName("e"):
    if symbol.getAttribute("oldname"):
      symbol.removeAttribute("oldname")
  out_filename = os.path.join(here, "..", "generated", "emoji4unicode.xml")
  emoji4unicode.Write(doc, out_filename)
  doc.unlink()


if __name__ == "__main__":
  main()
