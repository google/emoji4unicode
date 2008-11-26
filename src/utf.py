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

"""Unicode string helper functions for UTF-16/32 variability.

Python has changed from always-16-bit Unicode strings to
sometimes-16-bit/sometimes-32-bit Unicode strings,
as indicated by sys.maxunicode.

The helper functions here deal with the differences.
"""

__author__ = "Markus Scherer"

import sys

class _UTF16(object):
  @staticmethod
  def CodePointString(cp):
    return unichr(0xd7c0 + (cp >> 10)) + unichr(0xdc00 + (cp & 0x3ff))


class _UTF32(object):
  @staticmethod
  def CodePointString(cp):
    return unichr(cp)


if sys.maxunicode == 0xffff:
  UTF = _UTF16
elif sys.maxunicode == 0x10ffff:
  UTF = _UTF32
else:
  raise ValueError("unexpected sys.maxunicode = 0x%x" % sys.maxunicode)
