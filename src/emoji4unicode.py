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

"""Emoji symbols for the Unicode encoding proposal.

Reads emoji4unicode.xml, the carrier data files and other files
and makes the data available.

Attributes:
  carriers: List of lowercase names of carriers for which we have CarrierData.
  all_carrier_data: Map from lowercase carrier name to CarrierData object.
  arib_ucm: UCMFile with ARIB-Unicode mappings.
"""

__author__ = "Markus Scherer"

import os.path
import xml.dom.minidom
import carrier_data
import row_cell
import ucm

all_carrier_data = {}

def Load():
  """Parse emoji4unicode.xml and load related data."""
  # TODO(mscherer): Add argument for root data folder path.
  global carriers, all_carrier_data, arib_ucm, _doc, _root
  if all_carrier_data: return  # Already loaded.
  carriers = ["docomo", "kddi", "softbank", "google"]
  all_carrier_data = {
    "docomo": carrier_data.GetDocomoData(),
    "kddi": carrier_data.GetKddiData(),
    "softbank": carrier_data.GetSoftbankData(),
    "google": carrier_data.GetGoogleData()
  }
  here = os.path.dirname(__file__)
  arib_filename = os.path.join(here, "..", "data", "arib", "arib.ucm")
  arib_ucm = ucm.UCMFile(arib_filename)
  e4u_filename = os.path.join(here, "..", "data", "emoji4unicode.xml")
  _doc = xml.dom.minidom.parse(e4u_filename)
  _root = _doc.documentElement

def GetCategories():
  """Generator of Category objects."""
  global _root
  for element in _root.getElementsByTagName("category"):
    yield Category(element)

def GetSymbols():
  """Generator of Symbol objects."""
  for category in GetCategories():
    for subcategory in category.GetSubcategories():
      for symbol in subcategory.GetSymbols():
        yield symbol


class Category(object):
  """A category of Emoji symbols.

  Mostly a name string, and a container for subcategories.
  """
  def __init__(self, element):
    """Initialize from the Emoji4Unicode object and a <category> element.

    Do not instantiate directly: Use Emoji4Unicode.GetCategories().

    Args:
      element: <category> DOM element

    Raises:
      ValueError: If the element contains unexpected data.
    """
    self.__element = element
    self.name = element.getAttribute("name")
    self.in_proposal = _InProposal(element, True)

  def GetSubcategories(self):
    """Generator of Subcategory objects."""
    for element in self.__element.getElementsByTagName("subcategory"):
      yield Subcategory(self, element)


class Subcategory(object):
  """A subcategory of Emoji symbols.

  Mostly a name string, and a container for symbols.
  """
  def __init__(self, category, element):
    """Initialize from the Emoji4Unicode object and a <category> element.

    Do not instantiate directly: Use Emoji4Unicode.GetCategories().

    Args:
      category: Category object
      element: <subcategory> DOM element
    """
    self.__element = element
    self.name = element.getAttribute("name")
    self.category = category
    self.in_proposal = _InProposal(element, category.in_proposal)

  def GetSymbols(self):
    """Generator of Symbol objects."""
    for element in self.__element.getElementsByTagName("e"):
      yield Symbol(self, element)


class Symbol(object):
  """An Emoji symbol and its data.

  Attributes:
    id: Symbol ID as defined by and used for the Unicode encoding proposal.
  """
  __slots__ = "__element", "id", "subcategory", "in_proposal"

  def __init__(self, subcategory, element):
    """Initialize from the Emoji4Unicode object and an <e> element.

    Do not instantiate directly: Use Emoji4Unicode.GetSymbols() or
    Subcategory.GetSymbols().

    Args:
      element: <e> DOM element
    """
    self.__element = element
    self.id = element.getAttribute("id")
    self.subcategory = subcategory
    self.in_proposal = _InProposal(element, subcategory.in_proposal)

  def GetName(self):
    """Get the symbol's character name."""
    return self.__element.getAttribute("name")

  def ImageHTML(self):
    """Get the symbol's image HTML.

    Returns:
      An HTML string for the symbol's image, or an empty string if
      there is none.
    """
    img_from = self.__element.getAttribute("img_from")
    if img_from:
      global all_carrier_data
      from_carrier_data = all_carrier_data[img_from]
      carrier_uni = self.GetCarrierUnicode(img_from)
      return from_carrier_data.SymbolFromUnicode(carrier_uni).ImageHTML()
    return ""

  def GetTextRepresentation(self):
    """Get this symbol's text representation.

    Returns:
      The text representation string, or an empty string if there is none.
    """
    return self.__element.getAttribute("text_repr")

  def GetAnnotations(self):
    """Get the symbol's annotation lines.

    The annotation lines are collected for eventual inclusion in
    Unicode's NamesList.txt file.

    Returns:
      A list of strings, one per annotation line.
      The list may be empty.
    """
    annotations = []
    for element in self.__element.getElementsByTagName("ann"):
      annotations.append(element.firstChild.nodeValue.strip())
    return annotations

  def GetDescription(self):
    """Get the description text (may be empty)."""
    desc = self.__element.getElementsByTagName("desc")
    if desc:
      # We expect at most a single <desc> element with a text node.
      return desc[0].firstChild.nodeValue.strip()
    return ""

  def GetUnicode(self):
    """Get the Unicode code point or sequence with which this symbol is unified.

    Returns:
      A string with one or more 4..6-hex-digit code points with "+" separators,
      or an empty string if this symbol has not been unified with an existing
      character.
    """
    return self.__element.getAttribute("unicode")

  def GetARIB(self):
    """Get the code of the ARIB symbol corresponding to this Emoji symbol.

    Returns:
      The ARIB code as a 4-decimal-digit string,
      or None if there is no corresponding ARIB symbol.
    """
    uni = self.__element.getAttribute("unicode")
    if uni:
      global arib_ucm
      arib = arib_ucm.from_unicode.get(uni)
      if arib:
        return row_cell.FromShiftJisString(arib).ToDecimalString()
      else:
        return None

  def GetCarrierUnicode(self, carrier):
    """Get the carrier's Unicode PUA code point for this Emoji symbol.

    Returns:
      The Google code point as a 4..6-hex-digit string,
      or an empty string if there is none.
      The string may contain a '>' prefix for a fallback (one-way) mapping,
      in which case it may contain multiple codes separated by '+'.
    """
    global carriers
    if carrier not in carriers:
      raise ValueError("unknown carrier \"%s\"" % carrier)
    return self.__element.getAttribute(carrier)

  def GetTextFallback(self):
    """Get the text fallback for this Emoji symbol.

    Returns:
      The text fallback string,or an empty string if there is none.
    """
    return self.__element.getAttribute("text_fallback")


def _InProposal(element, parent_in_proposal):
  """Determine if a (sub)category or symbol is in the Unicode proposal.

  If the element node has an in_proposal attribute of "yes" or "no",
  then correspondingly return True/False.
  Otherwise inherit the value from the parent.

  Args:
    element: XML element for the (sub)category or symbol node
    parent_in_proposal: the parent's in_proposal value

  Returns:
    The resulting in_proposal value for this node
  """
  in_proposal_string = element.getAttribute("in_proposal")
  if in_proposal_string:
    if in_proposal_string == "yes":
      in_proposal = True
    elif in_proposal_string == "no":
      in_proposal = False
    else:
      raise ValueError("attribute value in_proposal=\"%s\" "
                        "not recognized" % in_proposal_string)
  else:
    in_proposal = parent_in_proposal
  return in_proposal
