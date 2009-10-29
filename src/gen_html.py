#!/usr/bin/python2.4
# encoding: UTF-8
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
import datetime
import everson
import sys
import emoji4unicode
import translit
import utf

# Flags from command-line options.
_only_in_proposal = False
_no_unified = False
_no_temp_notes = False
_no_fallbacks = False
_no_codes = False
_no_symbol_numbers = False
_show_font_chars = False
_show_only_font_chars = False
_with_everson = False
_eval_everson = False

_date = datetime.date.today().strftime("%Y-%b-%d")

_AUTHORS = u"""Authors:<br>
Markus Scherer, Mark Davis, Kat Momoi, Darick Tong (Google Inc.)<br>
Yasuo Kida, Peter Edberg (Apple Inc.)"""

_CSS = u"""
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
.id {
  text-align: center;
}
.code_point {
  text-align: center;
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
.everson_uni {
  color: magenta
}
.fontimg {
  height: 40;
  width: 40;
}
.efont {
  font-family: Apple Emoji;
  font-size: 36pt;
}
.everson_font_doc {
  color: magenta
}
.everson_font {
  font-family: Andreasmichael;
  font-size: 36pt;
  color: magenta
}
.status {
  font-size: 60%;
}
.old_name {
  font-weight: bold;
  color: red
}
.everson_name_anno {
  color: magenta
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
"""

_FULL_TABLE_HEADER = u"""
<table border='1' cellspacing='0' width='100%'>
<tr>
 <th>Internal ID</th>
 <th>Symbol</th>
 <th>Name &amp; Annotations</th>
 <th>DoCoMo</th>
 <th>KDDI</th>
 <th>SoftBank</th>
 <th>Google</th>
</tr>
"""

_HEADER = (u"""<html>
<title>Emoji Symbols: Background Data</title>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
""" +
_CSS +
u"""
</head>
<body>
<h1>Emoji Symbols: Background Data</h1>
<h2>Background data for Proposal for Encoding Emoji Symbols</h2>
<p align='right'>
  <span style='font-size:x-large'>L2/09-xxx</span><br>
  Date: """ + _date + u"<br>" +
_AUTHORS +
u"""</p>
<p>The carrier symbol images in this file point to images on other sites.
  The images are only for comparison and may change.</p>
<p>See the <a href="#legend">chart legend</a>
  for an explanation of the data presentation in this chart.</p>
<p>In the HTML version of this document,
  each symbol row has an anchor to allow direct linking by appending
  <a href="#e-4B0">#e-4B0</a> (for example) to this page's URL in the
  address bar.</p>
""" +
_FULL_TABLE_HEADER)

_FOOTER = u"""
<h2 id='legend'>Chart Legend</h2>
Columns:<br>
<ol><li>Internal ID: A unique identifier used only in the Emoji symbols encoding proposal and discussion. The IDs mostly follow the order of the symbols in the chart, but only for historical reasons, and some symbols have been moved while preserving their IDs. This is so that the IDs can serve as permanent identifiers throughout the review and proposal process.<br>
</li>
<li>Symbol: The symbol glyph, the code point, and its status.</li>
<ul><li>For a symbol proposed for new encoding, the proposed representative glyph is shown, the proposed code point is red, and the status text is "proposed".</li>
<li>For a symbol unified with an existing Unicode character, the code point is black and the status text is "unified". The glyph may differ from the Unicode chart glyph. In some cases, a symbol is unified with a sequence of existing characters.<br>
</li></ul>
<li>Name &amp; Annotations: The proposed character name for new symbols, or the name of the
existing or upcoming unified character. Optionally followed by further
information, if applicable:</li>
<ul>
<li>The old name, which is the character name proposed in a previous version of the document.</li>
<li>The ARIB code (4-decimal-digit row-cell code) of the corresponding <a href="http://sites.google.com/site/unicodesymbols/Home/japanese-tv-symbols">Japanese Broadcast Symbol</a>.</li>
<li>Proposed Unicode character annotations.</li>
<li>Free-form description text.</li>
<li>Font design instructions.<br>
</li></ul>
<li>DoCoMo/KDDI/SoftBank/Google: These columns show how each Emoji symbol maps to equivalent or similar symbols used by other companies.</li>
<ul><li>The table cell shows some or all of the following about each carrier's symbol:<br>
</li></ul>
<ul>
<ul><li>An image</li>
<li>A catalog number prefixed with '#'</li>
<ul><li>For SoftBank, these are the "new", post-June 2008 symbol numbers. "Old", pre-June 2008 symbol numbers are prefixed with '#old'.<br>
</li>
<li>For DoCoMo, numbers for "expansion" symbols are prefixed with '#Exp.'<br>
</li></ul>
<li>The English symbol name</li>
<li>The Japanese symbol name</li>
<li>A partial transliteration of the Japanese name if it contains Hiragana or Katakana<br>
</li>
<li>The Unicode Private Use Area (PUA) code point</li>
<li>The Shift-JIS code<br>
</li>
<li>The ISO 2022-JP code (based on JIS X 0208)</li></ul>
<li>If the carrier's symbol is not equivalent, the table cell may show a best-fit fallback mapping (one-way from proposal symbol ID to the carrier) to a carrier symbol or to a sequence of symbols.</li>
<ul><li>In this case, the table cell has golden background and a dotted cell border.</li>
<li>Sequences of codes are marked with + signs as separators.</li></ul>
<li>If there is no equivalent nor similar symbol, the table cell may show fallback text.</li>
<ul><li>In this case, the table cell has purple background, and there is no other information besides the fallback text. (In particular, no image.)</li>
<li>Types of text fallbacks:</li>
<ul><li>Fallback mappings to descriptive text rather than a symbol.</li>
<li>Fallback text to "ASCII art" (Kao Moji). Such
"ASCII art" may include fullwidth ASCII, Greek, Cyrillic and Han
characters — essentially anything available elsewhere in the character
set. For example: (&gt;人&lt;) for PERSON WITH FOLDED HANDS ("Sorry" or
"Please", KDDI Emoji 459, Softbank 376).<br>
</li>
<li>Fallback to the Geta Mark '〓' (U+3013).</li></ul></ul></ul>
</ol>
The carrier symbol images point to images on other sites. The images are only for comparison and may change.<br>
</body></html>"""

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
      symbols = []
      for symbol in subcategory.GetSymbols():
        if not symbol.in_proposal and _only_in_proposal:
          continue  # Skip this symbol.
        if symbol.GetUnicode():
          if _no_unified: continue  # Skip this symbol.
          number_symbols_unified += 1
        elif symbol.in_proposal:
          number_symbols_new += 1
        number_symbols_in_chart += 1
        symbols.append(symbol)
      if symbols:
        _WriteSingleCelledRow(writer,
                              "subcategory",
                              "%s (%s)" % (subcategory.name, category.name))
        _WriteFullSymbolRowsHTML(writer, symbols)
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

def _WriteFullSymbolRowsHTML(writer, symbols):
  for symbol in symbols:
    if symbol.in_proposal:
      row_style = ""
    else:
      row_style = " class=not_in_proposal"
    e_id = "e-" + symbol.id
    writer.write("<tr id=%s%s><td class='id'><a href=#%s>%s</a></td>" %
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


_PROPOSED_EMOJI_HEADER = (u"""<html>
<title>Emoji Symbols Proposed for New Encoding</title>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
""" +
_CSS +
u"""
</head>
<body>
<h1>Emoji Symbols Proposed for New Encoding</h1>
<h2>For the Proposal for Encoding Emoji Symbols</h2>
<p align='right'>
  <span style='font-size:x-large'>L2/09-xxx</span><br>
  Date: """ + _date + "<br>" +
_AUTHORS +
u"""</p>
<p>In the HTML version of this document,
  each symbol row has an anchor to allow direct linking by appending
  <a href="#e-4B0">#e-4B0</a> (for example) to this page's URL in the
  address bar.</p>
""")

_PROPOSED_EMOJI_TABLE_HEADER = u"""
<table border='1' cellspacing='0' width='100%'>
<tr>
  <th width='10%'>Code Point</th>
  <th width='10%'>Symbol</th>
  <th>Name &amp; Annotations</th>
  <th width='10%'>Internal ID</th>
</tr>
"""

_PROPOSED_EMOJI_FOOTER = u"""</body></html>"""

def _WriteProposedEmojiHTML(writer):
  proposed_symbols = emoji4unicode.GetSymbolsInProposalSortedByUnicode()
  number_symbols_new = 0
  writer.write(_PROPOSED_EMOJI_HEADER)
  prev_subcategory_name = ""
  for proposed_symbol in proposed_symbols:
    symbol = proposed_symbol[1]
    if symbol.GetUnicode(): continue  # Filter out unified symbols.
    number_symbols_new += 1
    subcategory_name = symbol.subcategory.name
    if prev_subcategory_name != subcategory_name:
      if prev_subcategory_name:
        writer.write("</table>\n")
      writer.write("<h3>%s</h3>" % subcategory_name)
      writer.write(_PROPOSED_EMOJI_TABLE_HEADER)
      prev_subcategory_name = subcategory_name
    e_id = "e-" + symbol.id
    writer.write("<tr id=%s>" % e_id)
    writer.write("<td class='code_point'>"
                 "<span class='proposed_uni'>U+%s</span></td>" %
                 symbol.GetProposedUnicode())
    font_uni = symbol.GetFontUnicode()
    font_str = utf.UTF.CodePointString(int(font_uni, 16))
    writer.write("<td class='rep'><span class='efont'>%s</span></td>" %
                 font_str)
    writer.write("<td class='name_anno'>%s</td>" % _NameAnnotationHTML(symbol))
    writer.write("<td class='id'><a href=#%s>%s</a></td>" %
                  (e_id, e_id))
    writer.write("</tr>\n")
  writer.write("</table>\n")
  writer.write("<p class='report'>Number of proposed new symbols: %d</p>\n" %
               number_symbols_new)
  writer.write(_PROPOSED_EMOJI_FOOTER)


_EVAL_EVERSON_HEADER = (u"""<html>
<title>Comments on specific changes suggested by """ + everson.doc +
u"""</title>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
""" +
_CSS +
u"""
</head>
<body>
<h1>Comments on specific changes suggested by """ + everson.doc + u"""</h1>
<p align='right'>
  <span style='font-size:x-large'>N36xx</span><br>
  <span style='font-size:x-large'>L2/09-xxx</span><br>
  Date: """ + _date + u"""<br>
  Authors:<br>
  Markus Scherer, Mark Davis, Kat Momoi</p>
<p>In the HTML version of this document,
  each symbol row has an anchor to allow direct linking by appending
  <a href="#e-4B0">#e-4B0</a> (for example) to this page's URL in the
  address bar.</p>
""")

_EVAL_EVERSON_FOOTER = u"""
<h2 id='legend'>Chart Legend</h2>
<p>Changes in """ + everson.doc + u""" compared with the US/UTC proposal
  are prefixed with \"""" + everson.doc + u""":\" and written in magenta.
  Each proposed symbol is shown with two glyphs,
  first the US/UTC (N3583) glyph,
  second the IE/DE (""" + everson.doc + u""") glyph.</p>
<p>The overall chart legend is available in
  <a href="http://www.unicode.org/L2/L2009/09026r-emoji-proposed.pdf">L2/09-026R</a>
  Emoji Symbols Proposed for New Encoding
  (=<a href="http://std.dkuug.dk/jtc1/sc2/wg2/docs/n3583.pdf">N3583</a>)
  and in <a href="http://sites.google.com/site/unicodesymbols/Home/emoji-symbols/chart-legend">http://sites.google.com/site/unicodesymbols/Home/emoji-symbols/chart-legend</a>.</p>
</body></html>"""

def _WriteEvalEversonHTML(writer):
  writer.write(_EVAL_EVERSON_HEADER)
  # Glyph changes.
  writer.write(u"""<h2>Glyph changes proposed in """ +
everson.doc + u"""</h2>
<p>We have reviewed the substantive glyph changes proposed in """ +
everson.doc + u""" for the following characters and
made a preliminary assessment.
The glyph changes for other characters are more difficult to evaluate
and are still being reviewed.</p>
""")
  symbols = everson.GetGoodGlyphChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"<h3>Good glyph changes</h3>\n")
    _WriteFullSymbolTableHTML(writer, symbols)
  symbols = everson.GetNeutralGlyphChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"<h3>Neutral glyph changes</h3>\n")
    _WriteFullSymbolTableHTML(writer, symbols)
  symbols = everson.GetSomewhatBadGlyphChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"<h3>Somewhat bad glyph changes</h3>\n")
    _WriteFullSymbolTableHTML(writer, symbols)
  symbols = everson.GetBadGlyphChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"<h3>Really bad glyph changes</h3>\n")
    _WriteFullSymbolTableHTML(writer, symbols)
  # Name changes.
  writer.write(u"""<h2>Name changes proposed in """ +
everson.doc + u"""</h2>
<p>We have reviewed the name changes proposed in """ +
everson.doc + u""" for the following characters and
made a preliminary assessment.
The name changes for other characters are more difficult to evaluate
and are still being reviewed.</p>
""")
  symbols = everson.GetGoodNameChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"<h3>Good name changes</h3>\n")
    _WriteFullSymbolTableHTML(writer, symbols)
  symbols = everson.GetNeutralNameChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"<h3>Neutral name changes</h3>\n")
    _WriteFullSymbolTableHTML(writer, symbols)
  symbols = everson.GetBadNameChanges(emoji4unicode.id_to_symbol)
  if symbols:
    writer.write(u"<h3>Bad name changes</h3>\n")
    _WriteFullSymbolTableHTML(writer, symbols)
  # Done.
  writer.write(_EVAL_EVERSON_FOOTER)


def _WriteFullSymbolTableHTML(writer, symbols):
  writer.write(u"<p>Number of changes: %d</p>\n" % len(symbols))
  writer.write(_FULL_TABLE_HEADER)
  _WriteFullSymbolRowsHTML(writer, symbols)
  writer.write("</table>\n")


_change_string = { 1: "good", 0: "neutral", -1: "bad", -2: "v.bad" }

def _EversonDocAndChangeString(change):
  if change == None:
    return everson.doc
  else:
    return everson.doc + u"(" + _change_string[change] + u")"


def _RepresentationHTML(e4u_symbol):
  """Return HTML with the symbol representation."""
  uni = e4u_symbol.GetUnicode()
  if uni:
    if e4u_symbol.IsUnifiedWithUpcomingCharacter() and not _show_font_chars:
      # Print only code points, not also characters,
      # because no one will have a font for these.
      # return (u"<span class='upcoming'>U5.2</span><br>"
      #          "U+" + uni.replace("+", " U+"))
      font_img = u"<img src='../uni52img/U+%s.jpg' class='fontimg'>" % uni
      repr = font_img + u"<br>U+" + uni.replace("+", " U+")
    else:
      repr = _UnicodeHTML(uni)
    return repr + u"<br><span class='status'>unified</span>"
  img = e4u_symbol.ImageHTML()
  font_uni = e4u_symbol.GetFontUnicode()
  font_img = u"<img src='../fontimg/AEmoji_%s.png' class='fontimg'>" % font_uni
  if e4u_symbol.in_proposal:
    if _show_font_chars:
      font_str = utf.UTF.CodePointString(int(font_uni, 16))
      if _show_only_font_chars:
        repr = u"<span class='efont'>%s</span>" % font_str
      else:
        repr = u"<span class='efont'>%s</span>=%s" % (font_str, font_img)
        if img: repr += u"\u2248" + img
    else:
      repr = font_img
    proposed_uni = e4u_symbol.GetProposedUnicode()
    if proposed_uni:
      repr += (u"<br><span class='proposed_uni'>U+" +
               proposed_uni.replace("+", " U+") + u"</span>")
      if _with_everson:
        everson_uni = everson.GetUnicode(e4u_symbol.id)
        if not everson_uni:
          numeric_id = int(e4u_symbol.id, 16)
          if not 0x554 <= numeric_id <= 0x56d:
            # Complain if a symbol proposed before WG2 N3607 does not
            # have N3607 data.
            sys.stderr.write(u"e-%s proposed U+%s missing Everson mapping\n" %
                             (e4u_symbol.id, proposed_uni))
        else:
          if _show_font_chars:
            font_str = utf.UTF.CodePointString(int(everson_uni, 16))
            repr += (u"<br><span class='everson_font_doc'>" +
                     _EversonDocAndChangeString(
                         everson.id_to_glyph_change.get(e4u_symbol.id)) +
                     u"</span>: <span class='everson_font'>%s</span>") % font_str
          if everson_uni != proposed_uni:
            repr += (u"<br><span class='everson_uni'>" +
                     everson.doc + u": U+" + everson_uni + u"</span>")
    else:
      repr += u"<br><span class='proposed_uni'>U+xxxxx</span>"
    return repr + u"<br><span class='status'>proposed</span>"
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
  return u"<span class='unified'>" + chars + u"</span><br>" + code_points[1:]


def _NameAnnotationHTML(e4u_symbol):
  """Return HTML with the symbol name, annotations, etc."""
  show_everson = False
  if _with_everson and e4u_symbol.in_proposal:
    proposed_uni = e4u_symbol.GetProposedUnicode()
    if proposed_uni:
      show_everson = True
  name = e4u_symbol.GetName()
  lines = [name]
  old_name = e4u_symbol.GetOldName()
  everson_uni = everson.GetUnicode(e4u_symbol.id)
  if show_everson and everson_uni:
    everson_name = everson.GetName(e4u_symbol.id)
    if everson_name != name or (old_name and everson_name != old_name):
      lines.append(u"<span class='everson_name_anno'>" +
                   _EversonDocAndChangeString(
                       everson.id_to_name_change.get(e4u_symbol.id)) +
                   u": " + everson_name + u"</span>")
  if old_name:
      lines.append(u"<span class='old_name'>Old name: " + old_name + u"</span>")
  arib = e4u_symbol.GetARIB()
  if arib: lines.append(u"<span class='arib'>= ARIB-%s</span>" % arib)
  if e4u_symbol.IsUnifiedWithUpcomingCharacter():
    lines.append(u"<span class='desc'>Temporary Note: "
                  "Unified with an upcoming Unicode 5.2/AMD6 character; "
                  "code point and name are preliminary.</span>")
  prop = e4u_symbol.GetProposedProperties()
  if prop: lines.append(u"Proposed Properties: " + prop)
  anno = e4u_symbol.GetAnnotations()
  for line in anno: lines.append(cgi.escape(line))
  if not _no_temp_notes:
    desc = e4u_symbol.GetDescription()
    if desc: lines.append(u"<span class='desc'>Temporary Notes: " +
                          cgi.escape(desc) + u"</span>")
    design = e4u_symbol.GetDesign()
    if design: lines.append(u"<span class='desc'>Design Note: " +
                            cgi.escape(design) + u"</span>")
  if show_everson and everson_uni:
    for line in everson.GetAnnotations(e4u_symbol.id):
      if line not in anno:
        lines.append(u"<span class='everson_name_anno'>" + everson.doc +
                    u": " + cgi.escape(line) + "</span>")
  return "<br>".join(lines)


def _CarrierSymbolHTML(carrier, one_carrier_data, code_string):
  codes = code_string.split("+")
  img_string = ""
  number_string = ""
  old_number_string = ""
  new_number_string = ""
  english_string = ""
  japanese_string = ""
  xlit_string = u""
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
    if name_ja:
      name_ja = name_ja.replace(u"\uFF08", u"(").replace(u"\uFF09", u")")
      japanese_string += "+" + name_ja
      xlit = translit.Transliterate(name_ja)
      xlit_string += u"+" + xlit
    if not _no_codes:
      uni_string += "+U+" + code
      if symbol.shift_jis: shift_jis_string += "+SJIS-" + symbol.shift_jis
      if symbol.jis: jis_string += "+JIS-" + symbol.jis
  if xlit_string:
    if xlit_string == japanese_string:
      xlit_string = u""
    else:
      xlit_string = u"+\u300C" + xlit_string[1:].replace(u"+", u"\u300D+\u300C") + u"\u300D"
  result_pieces = []
  if len(codes) == 1:
    # Reduce the cell height by putting multiple data pieces on each line.
    groups = [[img_string,
               number_string, old_number_string, new_number_string],
              [english_string, japanese_string, xlit_string],
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
                 english_string, japanese_string, xlit_string,
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
  global _only_in_proposal, _no_unified, _no_temp_notes, _no_fallbacks
  global _no_codes, _no_symbol_numbers, _show_font_chars, _show_only_font_chars
  global _with_everson, _eval_everson
  _proposed_by_unicode = False
  for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--only_in_proposal": _only_in_proposal = True
    if sys.argv[i] == "--no_codes": _no_codes = True
    if sys.argv[i] == "--proposed_by_unicode":
      _no_temp_notes = True
      _proposed_by_unicode = True
    if sys.argv[i] == "--show_only_font_chars":
      _show_font_chars = True
      _show_only_font_chars = True
    if sys.argv[i] == "--design":
      _only_in_proposal = True
      _no_unified = True
      _no_fallbacks = True
      _no_codes = True
      _no_symbol_numbers = True
      _show_font_chars = True
    if sys.argv[i] == "--everson": _with_everson = True
    if sys.argv[i] == "--eval_everson":
      _eval_everson = True
      _with_everson = True
  emoji4unicode.Load()
  if _with_everson: everson.Load()
  writer = codecs.getwriter("UTF-8")(sys.stdout)
  if _eval_everson:
    _WriteEvalEversonHTML(writer)
  elif _proposed_by_unicode:
    _WriteProposedEmojiHTML(writer)
  else:
    _WriteEmoji4UnicodeHTML(writer)

if __name__ == "__main__":
  main()
