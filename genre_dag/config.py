#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

BASE_URL = "https://en.wikipedia.org/wiki/"
# browser settings
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)"
           " Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1"}
BASE_PATH = os.getcwd()
DATA_PATH = os.path.join(BASE_PATH, "data/")
