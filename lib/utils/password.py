#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Penework opensource framework
See the file 'docs/COPYING' for copying permission
"""

from lib.core.common import getFileItems
from lib.core.data import paths


def getWeakPassword():
    return getFileItems(paths.WEAK_PASS)


def getLargeWeakPassword():
    return getFileItems(paths.LARGE_WEAK_PASS)
