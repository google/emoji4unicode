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

"""Update emoji4unicode.xml from a NamesList.txt file.

During the development of Unicode 6.0/ISO 10646 AMD8,
Emoji symbols may change code points, names, and annotations.
This script reads emoji4unicode.xml and a NamesList.txt file,
updates the XML data according to the NamesList,
and writes a modified XML file to stdout.
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
  id_to_symbol = {}
  for symbol in root.getElementsByTagName("e"):
    id_to_symbol[symbol.getAttribute("id")] = symbol
  nameslist_filename = os.path.join(here, "..", "data",
                                    "unicode", "uc60-a-PDAM8-Dublin.lst")
  for record in nameslist.Read(nameslist_filename):
    if "uni" not in record:
      continue
    id = nameslist.GetEmojiID(record)
    if not id:
      continue
    # Extract the old data from the emoji4unicode.xml <e> symbol element.
    symbol = id_to_symbol[id]
    old_uni = symbol.getAttribute("unicode")
    old_name = symbol.getAttribute("name")
    old_annotations = []
    for element in symbol.getElementsByTagName("ann"):
      old_annotations.append(element.firstChild.nodeValue.strip())
    # Extract the new data from the NamesList record.
    new_uni = record["uni"]
    new_name = record["name"]
    new_annotations = record["data"]
    # Update the proposed Unicode code point.
    if old_uni and not old_uni.startswith("+"):
      print ("*** e-%s: setting proposed code point %s but " +
             "old %s was not proposed" %
             (id, new_uni, old_uni))
    symbol.setAttribute("unicode", u"+" + new_uni)
    # Update the proposed character name.
    # Keep the previous name in an oldname attribute.
    if False:  # TODO: Turn on name changes.
      if old_name == new_name:
        if symbol.getAttribute("oldname"):
          symbol.removeAttribute("oldname")
      else:
        symbol.setAttribute("oldname", old_name)
        symbol.setAttribute("name", new_name)
    # Append new annotations.
    if False:  # TODO: Turn on adding annotations.
      for ann in new_annotations:
        # Skip the Emoji symbol ID alias, and annotations that are not new.
        if not ann.startswith(u"= e-") and ann not in old_annotations:
          ann_element = doc.createElement("ann")
          ann_element.appendChild(doc.createTextNode(ann))
          symbol.appendChild(ann_element)
  out_filename = os.path.join(here, "..", "generated", "emoji4unicode.xml")
  emoji4unicode.Write(doc, out_filename)
  doc.unlink()


if __name__ == "__main__":
  main()
