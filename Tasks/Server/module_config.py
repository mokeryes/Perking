#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-21 16:08:45
# @Description : 配置包的路径
"""

import sys
from os.path import abspath, join, dirname

def insert_path():
    sys.path.insert(0, join(abspath(dirname(__file__)), '../../Sources/'))
