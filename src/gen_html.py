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

"""Generate an HTML chart with the emoji4unicode.xml and related data."""

__author__ = "Darick Tong"
__author__ = "Markus Scherer"

import cgi
import codecs
import sys
import emoji4unicode
import utf

# Flags from command-line options.
_only_in_proposal = False
_no_unified = False
_no_fallbacks = False
_no_codes = False
_no_symbol_numbers = False
_show_font_chars = False

_HEADER = """<html>
<title>Table for Working Draft Proposal for Encoding Emoji Symbols</title>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
<style>
body {
  font-family: Arial, Helvetica, Sans-serif;
}
.category {
  font-weight: bold;
  font-size: 110%;
  background: #C8C8C8;
}
.subcategory {
  font-weight: bold;
  background: #EEE;
}
.not_in_proposal {
  text-decoration: line-through;
}
.rep {
  text-align: center;
}
.unified {
  font-size: 36pt;
}
.upcoming {
  font-size: 24pt;
  font-stretch: ultra-condensed;
  font-style: italic;
}
.proposed_uni {
  color: red
}
.fontimg {
  height: 40;
  width: 40;
}
.efont {
  font-family: Apple Emoji;
}
.name_anno {
  font-size: 80%;
}
.arib {
  color: gray;
}
.desc {
  color: gray;
}
.design {
  color: gray;
}
.pua, .imgs, .translit {
  text-align: center;
}
.num {
  text-align: right;
}
.round_trip {
}
.fallback {
  background:#FFCC00;
  border-style: dotted;
  border-width: 2px
}
.text_fallback {
  background:#CC99FF;
}
.no_mapping {
}
.report {
  font-weight: bold;
}
</style>
</head>
<body>
<h1>Table for Working Draft Proposal for Encoding Emoji Symbols</h1>
<p>The images in this file point to images on other sites.
  The images are only for comparison and may change.</p>
<p>If the proposal font is available, then the Symbol column shows the proposal
  font glyphs for symbols that are proposed for addition to the Unicode
  Standard. If the proposal font is not available, then unrelated glyphs from
  other installed fonts will be visible in the Symbol column.</p>
<p>See the <a href="http://sites.google.com/site/unicodesymbols/Home/emoji-symbols/chart-legend">chart legend</a>
  for an explanation of the data presentation in this chart.</p>
<p>Each symbol row has an anchor to allow direct linking by appending
  <a href="#e-4B0">#e-4B0</a> (for example) to this page's URL in the
  address bar.</p>
<table border='1' cellspacing='0' width='100%'>
<tr>
 <th>Symbol ID</th>
 <th>Symbol</th>
 <th>Name &amp; Annotations</th>
 <th>DoCoMo</th>
 <th>KDDI</th>
 <th>SoftBank</th>
 <th>Google</th>
</tr>
"""

_FOOTER = """</body></html>"""

def _WriteEmoji4UnicodeHTML(writer):
  number_symbols_in_chart = 0
  number_symbols_unified = 0
  number_symbols_new = 0
  writer.write(_HEADER)
  for category in emoji4unicode.GetCategories():
    category_string = category.name
    if not category.in_proposal:
      if _only_in_proposal: continue  # Skip this category.
      category_string += (" (This section is for comparison only -- "
                          "not part of the Emoji proposal.)")
    _WriteSingleCelledRow(writer, "category", category_string)
    for subcategory in category.GetSubcategories():
      if not subcategory.in_proposal and _only_in_proposal:
        continue  # Skip this subcategory.
      _WriteSingleCelledRow(writer,
                            "subcategory",
                            "%s (%s)" % (subcategory.name, category.name))
      for symbol in subcategory.GetSymbols():
        if symbol.in_proposal:
          row_style = ""
        elif _only_in_proposal:
          continue  # Skip this symbol.
        else:
          row_style = " class=not_in_proposal"
        if symbol.GetUnicode():
          if _no_unified: continue  # Skip this symbol.
          number_symbols_unified += 1
        elif symbol.in_proposal:
          number_symbols_new += 1
        number_symbols_in_chart += 1
        e_id = "e-" + symbol.id
        writer.write("<tr id=%s%s><td><a href=#%s>%s</a></td>" %
                     (e_id, row_style, e_id, e_id))
        writer.write("<td class='rep'>%s</td>" % _RepresentationHTML(symbol))
        writer.write("<td class='name_anno'>%s</td>" % _NameAnnotationHTML(symbol))
        for carrier in emoji4unicode.carriers:
          code = symbol.GetCarrierUnicode(carrier)
          if code:
            if code.startswith(">"):
              if _no_fallbacks:
                writer.write("<td class='no_mapping'>-</td>")
                continue
              template = "<td class='fallback'>%s</td>"
              code = code[1:]
            else:
              template = "<td class='round_trip'>%s</td>"
            cell = template % _CarrierSymbolHTML(
                carrier,
                emoji4unicode.all_carrier_data[carrier],
                code)
          elif _no_fallbacks:
            cell = "<td class='no_mapping'>-</td>"
          else:
            text_fallback = symbol.GetTextFallback()
            if not text_fallback: text_fallback = u"\u3013"  # geta mark
            cell = "<td class='text_fallback'>%s</td>" % text_fallback
          writer.write(cell)
        writer.write("</tr>\n")
  writer.write("</table>\n")
  writer.write("<p class='report'>Number of symbols in this chart: %d</p>\n" %
               number_symbols_in_chart)
  if _no_unified:
    writer.write("<p class='report'>Number of symbols unified with existing "
                 "Unicode characters: None shown in this chart.</p>\n")
  else:
    writer.write("<p class='report'>Number of symbols unified with existing "
                 "Unicode characters: %d</p>\n" %
                 number_symbols_unified)
  writer.write("<p class='report'>Number of proposed new symbols: %d</p>\n" %
               number_symbols_new)
  writer.write(_FOOTER)


def _RepresentationHTML(e4u_symbol):
  """Return HTML with the symbol representation."""
  uni = e4u_symbol.GetUnicode()
  if uni:
    if e4u_symbol.IsUnifiedWithUpcomingCharacter():
      # Print only code points, not also characters,
      # because no one will have a font for these.
      return (u"<span class='upcoming'>U5.2</span><br>"
               "U+" + uni.replace("+", " U+"))
    else:
      return _UnicodeHTML(uni)
  img = e4u_symbol.ImageHTML()
  font_uni = e4u_symbol.GetFontUnicode()
  font_img = u"<img src='../fontimg/AEmoji_%s.png' class='fontimg'>" % font_uni
  if e4u_symbol.in_proposal:
    glyph_id = e4u_symbol.GetGlyphRefID()
    if _show_font_chars:
      font_str = utf.UTF.CodePointString(int(font_uni, 16))
      repr = (u"<span class='efont'>%s</span><sub>glyph%d</sub>=%s" %
              (font_str, glyph_id, font_img))
      if img: repr += u"\u2248" + img
    else:
      # repr = u"glyph%d" % glyph_id
      repr = font_img
    proposed_uni = e4u_symbol.GetProposedUnicode()
    if proposed_uni:
      return (repr + u"<br><span class='proposed_uni'>U+" +
              proposed_uni.replace("+", " U+"))
    else:
      return repr + u"<br><span class='proposed_uni'>U+xxxxx</span>"
  if img: return img
  text_repr = e4u_symbol.GetTextRepresentation()
  if text_repr: return text_repr
  return "?repr?"


def _UnicodeHTML(uni):
  """Turn '0041+005A' into pretty HTML.

  Args:
    uni: Input string like '0041' or '0041+005A'.

  Returns:
    Corresponding pretty HTML.
  """
  # Turn '0041+005A' into 'Az U+0041 U+005A'.
  chars = unicode()
  code_points = unicode()
  for code in uni.split("+"):
    chars += utf.UTF.CodePointString(int(code, 16))
    code_points += " U+" + code
  return (u"<span class='unified'>" + chars + u"</span>" + u"<br>" +
          code_points[1:])


def _NameAnnotationHTML(e4u_symbol):
  """Return HTML with the symbol name, annotations, etc."""
  lines = [e4u_symbol.GetName()]
  arib = e4u_symbol.GetARIB()
  if arib: lines.append(u"<span class='arib'>= ARIB-%s</span>" % arib)
  if e4u_symbol.IsUnifiedWithUpcomingCharacter():
    lines.append(u"<span class='desc'>Temporary Note: "
                  "Unified with an upcoming Unicode 5.2/AMD6 character; "
                  "code point and name are preliminary.</span>")
  for line in e4u_symbol.GetAnnotations(): lines.append(cgi.escape(line))
  desc = e4u_symbol.GetDescription()
  if desc: lines.append(u"<span class='desc'>Temporary Notes: " +
                        cgi.escape(desc) + u"</span>")
  design = e4u_symbol.GetDesign()
  if design: lines.append(u"<span class='desc'>Design Note: " +
                          cgi.escape(design) + u"</span>")
  return "<br>".join(lines)


def _CarrierSymbolHTML(carrier, one_carrier_data, code_string):
  codes = code_string.split("+")
  img_string = ""
  number_string = ""
  old_number_string = ""
  new_number_string = ""
  english_string = ""
  japanese_string = ""
  uni_string = ""
  shift_jis_string = ""
  jis_string = ""
  for code in codes:
    symbol = one_carrier_data.SymbolFromUnicode(code)
    img_html = emoji4unicode.CarrierImageHTML(carrier, symbol)
    if img_html: img_string += "+%s" % img_html
    if not _no_symbol_numbers:
      if symbol.number:
        if carrier == "docomo" and symbol.number >= 300:
          # DoCoMo shows symbol numbers 1..176 for "Basic Pictograms" and
          # symbol numbers "Exp.1".."Exp.76" in the English publication of
          # "Expansion Pictograms".
          # Our data uses an offset of 300 for the integer numbers of
          # Expansion Pictograms.
          number_string += "+#Exp." + str(symbol.number - 300)
        else:
          number_string += "+#" + str(symbol.number)
      if symbol.old_number:
        old_number_string += "+#old" + str(symbol.old_number)
      if symbol.new_number:
        new_number_string += "+#new" + str(symbol.new_number)
    name_en = symbol.GetEnglishName()
    if name_en: english_string += "+'%s'" % name_en
    name_ja = symbol.GetJapaneseName()
    if name_ja: japanese_string += "+" + name_ja
    if not _no_codes:
      uni_string += "+U+" + code
      if symbol.shift_jis: shift_jis_string += "+SJIS-" + symbol.shift_jis
      if symbol.jis: jis_string += "+JIS-" + symbol.jis
  result_pieces = []
  if len(codes) == 1:
    # Reduce the cell height by putting multiple data pieces on each line.
    groups = [[img_string,
               number_string, old_number_string, new_number_string],
              [english_string, japanese_string],
              [uni_string],
              [shift_jis_string, jis_string]]
    for group in groups:
      group_pieces = []
      for line in group:
        if line: group_pieces.append(line[1:])  # Remove leading separator.
      if group_pieces: result_pieces.append(" ".join(group_pieces))
  else:
    # For code sequences, use a line per type of data.
    for line in (img_string,
                 number_string, old_number_string, new_number_string,
                 english_string, japanese_string,
                 uni_string, shift_jis_string, jis_string):
      if line: result_pieces.append(line[1:])  # Remove leading separator.
  if not result_pieces:
    # Show *something* despite _no_codes.
    return u"-"
  return "<br>".join(result_pieces)


def _WriteSingleCelledRow(writer, style, contents):
  """Writes a single cell that spans an entire row."""
  writer.write("<tr><td class='%s' colspan=7>%s</td></tr>\n" % (style, contents))


def main():
  global _only_in_proposal, _no_unified, _no_fallbacks
  global _no_codes, _no_symbol_numbers, _show_font_chars
  for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--only_in_proposal": _only_in_proposal = True
    if sys.argv[i] == "--no_codes": _no_codes = True
    if sys.argv[i] == "--design":
      _only_in_proposal = True
      _no_unified = True
      _no_fallbacks = True
      _no_codes = True
      _no_symbol_numbers = True
      _show_font_chars = True
  emoji4unicode.Load()
  _WriteEmoji4UnicodeHTML(codecs.getwriter("UTF-8")(sys.stdout))


if __name__ == "__main__":
  main()
