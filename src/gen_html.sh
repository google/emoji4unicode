#!/bin/bash
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
#
# Author: Markus Scherer

mkdir -p ../generated
# The full chart with all information.
./gen_html.py > ../generated/full.html
# All information, but only with the symbols that are in the proposal.
./gen_html.py --only_in_proposal > ../generated/utc.html
# All symbols, but shorter format. Omits carrier character codes.
./gen_html.py --no_codes > ../generated/short.html
# Special chart for the font and glyph design.
# ./gen_html.py --design > ../generated/design.html
# Special chart with only the symbols proposed for new encoding,
# sorted by Unicode code points.
./gen_html.py --proposed_by_unicode --show_only_font_chars > ../generated/proposed.html
# All information, but only with the symbols that are in the proposal.
# Same as utc.html but uses the fonts rather than the images.
./gen_html.py --only_in_proposal --show_only_font_chars > ../generated/utc_pdf.html
# All information, except category names, temporary and design notes;
# sorted by Unicode code points.
./gen_html.py --emoji_data > ../generated/emojidata.html
