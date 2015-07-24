#!/usr/bin/env python

import sys

PYTHON3 = sys.version_info[0] == 3
if PYTHON3:
    text_type = str
else:
    text_type = unicode  # NOQA
