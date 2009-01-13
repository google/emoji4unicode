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

"""Mini-transliteration service."""

__author__ = "Markus Scherer"

_TRANSLIT_TABLE = {
  u"\u3041": u"a",
  u"\u3042": u"a",
  u"\u3043": u"i",
  u"\u3044": u"i",
  u"\u3045": u"u",
  u"\u3046": u"u",
  u"\u3047": u"e",
  u"\u3048": u"e",
  u"\u3049": u"o",
  u"\u304A": u"o",
  u"\u304B": u"ka",
  u"\u304C": u"ga",
  u"\u304D": u"ki",
  u"\u304E": u"gi",
  u"\u304F": u"ku",
  u"\u3050": u"gu",
  u"\u3051": u"ke",
  u"\u3052": u"ge",
  u"\u3053": u"ko",
  u"\u3054": u"go",
  u"\u3055": u"sa",
  u"\u3056": u"za",
  u"\u3057": u"si",
  u"\u3058": u"zi",
  u"\u3059": u"su",
  u"\u305A": u"zu",
  u"\u305B": u"se",
  u"\u305C": u"ze",
  u"\u305D": u"so",
  u"\u305E": u"zo",
  u"\u305F": u"ta",
  u"\u3060": u"da",
  u"\u3061": u"ti",
  u"\u3062": u"di",
  u"\u3063": u"tu",
  u"\u3064": u"tu",
  u"\u3065": u"du",
  u"\u3066": u"te",
  u"\u3067": u"de",
  u"\u3068": u"to",
  u"\u3069": u"do",
  u"\u306A": u"na",
  u"\u306B": u"ni",
  u"\u306C": u"nu",
  u"\u306D": u"ne",
  u"\u306E": u"no",
  u"\u306F": u"ha",
  u"\u3070": u"ba",
  u"\u3071": u"pa",
  u"\u3072": u"hi",
  u"\u3073": u"bi",
  u"\u3074": u"pi",
  u"\u3075": u"hu",
  u"\u3076": u"bu",
  u"\u3077": u"pu",
  u"\u3078": u"he",
  u"\u3079": u"be",
  u"\u307A": u"pe",
  u"\u307B": u"ho",
  u"\u307C": u"bo",
  u"\u307D": u"po",
  u"\u307E": u"ma",
  u"\u307F": u"mi",
  u"\u3080": u"mu",
  u"\u3081": u"me",
  u"\u3082": u"mo",
  u"\u3083": u"ya",
  u"\u3084": u"ya",
  u"\u3085": u"yu",
  u"\u3086": u"yu",
  u"\u3087": u"yo",
  u"\u3088": u"yo",
  u"\u3089": u"ra",
  u"\u308A": u"ri",
  u"\u308B": u"ru",
  u"\u308C": u"re",
  u"\u308D": u"ro",
  u"\u308E": u"wa",
  u"\u308F": u"wa",
  u"\u3090": u"wi",
  u"\u3091": u"we",
  u"\u3092": u"wo",
  u"\u3093": u"n",
  u"\u3094": u"vu",
  u"\u3095": u"ka",
  u"\u3096": u"ke",
  u"\u30A1": u"a",
  u"\u30A2": u"a",
  u"\u30A3": u"i",
  u"\u30A4": u"i",
  u"\u30A5": u"u",
  u"\u30A6": u"u",
  u"\u30A7": u"e",
  u"\u30A8": u"e",
  u"\u30A9": u"o",
  u"\u30AA": u"o",
  u"\u30AB": u"ka",
  u"\u30AC": u"ga",
  u"\u30AD": u"ki",
  u"\u30AE": u"gi",
  u"\u30AF": u"ku",
  u"\u30B0": u"gu",
  u"\u30B1": u"ke",
  u"\u30B2": u"ge",
  u"\u30B3": u"ko",
  u"\u30B4": u"go",
  u"\u30B5": u"sa",
  u"\u30B6": u"za",
  u"\u30B7": u"si",
  u"\u30B8": u"zi",
  u"\u30B9": u"su",
  u"\u30BA": u"zu",
  u"\u30BB": u"se",
  u"\u30BC": u"ze",
  u"\u30BD": u"so",
  u"\u30BE": u"zo",
  u"\u30BF": u"ta",
  u"\u30C0": u"da",
  u"\u30C1": u"ti",
  u"\u30C2": u"di",
  u"\u30C3": u"tu",
  u"\u30C4": u"tu",
  u"\u30C5": u"du",
  u"\u30C6": u"te",
  u"\u30C7": u"de",
  u"\u30C8": u"to",
  u"\u30C9": u"do",
  u"\u30CA": u"na",
  u"\u30CB": u"ni",
  u"\u30CC": u"nu",
  u"\u30CD": u"ne",
  u"\u30CE": u"no",
  u"\u30CF": u"ha",
  u"\u30D0": u"ba",
  u"\u30D1": u"pa",
  u"\u30D2": u"hi",
  u"\u30D3": u"bi",
  u"\u30D4": u"pi",
  u"\u30D5": u"hu",
  u"\u30D6": u"bu",
  u"\u30D7": u"pu",
  u"\u30D8": u"he",
  u"\u30D9": u"be",
  u"\u30DA": u"pe",
  u"\u30DB": u"ho",
  u"\u30DC": u"bo",
  u"\u30DD": u"po",
  u"\u30DE": u"ma",
  u"\u30DF": u"mi",
  u"\u30E0": u"mu",
  u"\u30E1": u"me",
  u"\u30E2": u"mo",
  u"\u30E3": u"ya",
  u"\u30E4": u"ya",
  u"\u30E5": u"yu",
  u"\u30E6": u"yu",
  u"\u30E7": u"yo",
  u"\u30E8": u"yo",
  u"\u30E9": u"ra",
  u"\u30EA": u"ri",
  u"\u30EB": u"ru",
  u"\u30EC": u"re",
  u"\u30ED": u"ro",
  u"\u30EE": u"wa",
  u"\u30EF": u"wa",
  u"\u30F0": u"wi",
  u"\u30F1": u"we",
  u"\u30F2": u"wo",
  u"\u30F3": u"n",
  u"\u30F4": u"vu",
  u"\u30F5": u"ka",
  u"\u30F6": u"ke",
  u"\u30F7": u"va",
  u"\u30F8": u"vi",
  u"\u30F9": u"ve",
  u"\u30FA": u"vo"
}

def Transliterate(s):
  """Transform the string according to our mini-transliteration.

  Args:
    s: Input string.

  Returns:
    (Partially) transliterated version of the input string.
  """
  index = 0
  while index < len(s):
    if s[index] in _TRANSLIT_TABLE:
      replacement = _TRANSLIT_TABLE[s[index]]
      s = s[:index] + replacement + s[index + 1:]
      index += len(replacement)
    elif s[index] == u"\u30FC":
      # PROLONGED SOUND MARK
      # Assume that the preceding character was a normal syllable and
      # was transliterated.
      s = s[:index] + s[index - 1] + s[index + 1:]
      index = index + 1
    else:
      index = index + 1
  return s
