#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Penework opensource framework
See the file 'docs/COPYING' for copying permission
"""
import os


def initial():
    currentUserHomePath = os.path.expanduser('~')
    _ = """[zoomeye]\nusername = Your ZoomEye Username\npassword = Your ZoomEye Password\n\n[token]\nseebug = Your Seebug Token"""
    if not os.path.isfile(currentUserHomePath + '/.peneworkrc'):
        with open(currentUserHomePath + '/.peneworkrc', 'w') as fp:
            fp.write(_)

initial()
