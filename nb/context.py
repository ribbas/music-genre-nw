#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SRC_PATH)

from genre_dag.util import read_json

DATA_PATH = os.path.join((os.path.dirname(os.getcwd())), "data")

data = read_json(DATA_PATH + "/data.json")
