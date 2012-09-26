#!/usr/bin/python2.6
#
# Copyright 2012 Google Inc.
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

"""Generate Unicode Emoji conversion files."""

__author__ = "Markus Scherer"

import codecs
import os.path
import re
import sys
import emoji4unicode
import row_cell

def _CarrierSymbolToBytes(carrier_symbol, for_sjis):
  """Takes a single carrier private use Unicode code point and returns
  the carrier charset bytes for it, each byte prefixed with \\x."""
  if for_sjis:
    if not carrier_symbol.shift_jis: return ""
    carrier_bytes = carrier_symbol.shift_jis.replace("+", "")
  else:
    # The ICU ISO-2022-JP converter works with a Shift-JIS table.
    # Convert the JIS X 0208 codes to the corresponding Shift-JIS codes.
    if not carrier_symbol.jis: return ""
    carrier_bytes = ""
    for jis in carrier_symbol.jis.split("+"):
      carrier_bytes += row_cell.From2022String(jis).ToShiftJisString()
  b = ""
  for i in xrange(0, len(carrier_bytes), 2):
    b += u"\\x" + carrier_bytes[i:i + 2]
  return b


def _WriteMappings(writer, carrier, for_sjis):
  """Writes Emoji carrier mappings in ICU .ucm format."""
  carrier_data = emoji4unicode.all_carrier_data[carrier]
  gpua_fallbacks = []
  writer.write(u"# Mappings for Unicode Standard Emoji symbols.\n")
  symbols = emoji4unicode.GetSymbolsSortedByUnicode()
  for (cp_list, symbol) in symbols:
    code = symbol.GetCarrierUnicode(carrier)
    if not code: continue
    if code.startswith(">"):
      code = code[1:]
      precision = "|1"  # fallback mapping
    else:
      precision = "|0"  # roundtrip mapping
    b = ""
    complete = True
    for one_code in code.split("+"):
      carrier_symbol = carrier_data.SymbolFromUnicode(one_code)
      one_code_bytes =  _CarrierSymbolToBytes(carrier_symbol, for_sjis)
      if one_code_bytes:
        if b:
          b += "+" + one_code_bytes
        else:
          b = one_code_bytes
      else:
        complete = False
    if not complete: continue
    uni = "+".join([u"<U%04X>" % cp for cp in cp_list])
    writer.write(u"%s %s %s\n" % (uni, b, precision))
    # Variation Selector sequences:
    # It is easiest to have the conversion code ignore/drop
    # Variation Selectors and other Default_Ignorable_Code_Point,
    # rather than adding them to the mapping table.
    #
    # However, we do need to add explicit sequences with Variation Selectors
    # if the VS goes into the middle of the sequence because otherwise
    # the converter's longest-match algorithm fails to find the sequence.
    #
    # The conversion code is expected to use fallback mappings with
    # Variation Selectors even if normal fallbacks are turned off.
    # This is problematic if the symbol without VS has only a fallback mapping,
    # that is, precision == "|0":
    # The converter might not have enough logic to determine that such a
    # fallback-sequence-with-VS should not be used.
    if symbol.UnicodeHasVariationSequence() and len(cp_list) >= 2:
      # Add fallback mappings from "text style" and "emoji style"
      # Variation Selector sequences.
      vs_list = cp_list
      # Insert the variation selector before a combining mark,
      # in particular before the U+20E3 Combining Enclosing Keycap.
      # Given the current mappings, the variation selector is always
      # the second code point.
      vs_list.insert(1, 0xfe0e)  # VS15 for text style
      uni = "+".join([u"<U%04X>" % cp for cp in vs_list])
      writer.write(u"%s %s |1\n" % (uni, b))
      vs_list[1] = 0xfe0f  # VS16 for emoji style
      uni = "+".join([u"<U%04X>" % cp for cp in vs_list])
      writer.write(u"%s %s |1\n" % (uni, b))
    if cp_list[0] < 0xF0000:
      google_uni = symbol.GetCarrierUnicode("google")
      if google_uni:
        if google_uni.startswith(">"):
          if precision == "|1": continue  # no reverse fallback from a fallback
          google_uni = google_uni[1:]
          reverse_precision = "|3"  # reverse fallback _to_ Google PUA
        else:
          reverse_precision = "|1"  # legacy fallback _from_ Google PUA
        gpua_fallbacks.append(u"<U%s> %s %s\n" %
                              (google_uni, b, reverse_precision))
  writer.write(u"# Fallbacks for Google PUA code points, "
                "for Unicode Standard Emoji symbols.\n")
  gpua_fallbacks.sort()
  for fallback in gpua_fallbacks:
    writer.write(fallback)


def _WritePartialMappingFile(path, carrier, for_sjis):
  type = "shift_jis" if for_sjis else "jisx_208"
  filename = os.path.join(path, "%s-%s-partial.ucm" % (carrier, type))
  writer = codecs.open(filename, "w", "UTF-8")
  _WriteMappings(writer, carrier, for_sjis)
  writer.close()


_lead_byte_re = re.compile(u"^<U.+> +\\\\x([0-9A-Fa-f]{2})")

def _WriteCompleteMappingFile(sjis_reader, path, carrier, for_sjis):
  sjis_reader.seek(0, 0)
  carrier_data = emoji4unicode.all_carrier_data[carrier]
  if for_sjis:
    lead_bytes = carrier_data.GetShiftJISLeadBytes()
  else:
    lead_bytes = carrier_data.GetJISLeadBytesAsShiftJIS()
  type = "shift_jis" if for_sjis else "jisx_208"
  filename = os.path.join(path, "%s-%s-2012.ucm" % (carrier, type))
  with codecs.open(filename, "w", "UTF-8") as writer:
    for line in sjis_reader:
      if line.startswith("END CHARMAP"):
        _WriteMappings(writer, carrier, for_sjis)
      # Copy all lines except for those with mappings with Emoji lead bytes.
      match = _lead_byte_re.match(line)
      if not match or int(match.group(1), 16) not in lead_bytes:
        writer.write(line)


def main():
  emoji4unicode.Load()
  here = os.path.dirname(__file__)
  path = os.path.join(here, "..", "generated")
  _WritePartialMappingFile(path, "docomo", True)
  _WritePartialMappingFile(path, "docomo", False)
  _WritePartialMappingFile(path, "kddi", True)
  _WritePartialMappingFile(path, "kddi", False)
  _WritePartialMappingFile(path, "softbank", True)
  # We do not have JIS mapping data for SoftBank.

  if len(sys.argv) >= 2:
    # Use a custom Shift-JIS table as the base.
    sjis_filename = sys.argv[1]
  else:
    # Use the Windows Shift-JIS table as the base.
    sjis_filename = os.path.join(here, "..",
                                 "data", "icu", "windows-932-2000.ucm")
  with codecs.open(sjis_filename, "r") as sjis_reader:
    _WriteCompleteMappingFile(sjis_reader, path, "docomo", True)
    _WriteCompleteMappingFile(sjis_reader, path, "docomo", False)
    _WriteCompleteMappingFile(sjis_reader, path, "kddi", True)
    _WriteCompleteMappingFile(sjis_reader, path, "kddi", False)
    _WriteCompleteMappingFile(sjis_reader, path, "softbank", True)
    # We do not have JIS mapping data for SoftBank.


if __name__ == "__main__":
  main()
