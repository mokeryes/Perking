#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 19:17:33
# @Description : 将有单位的计数转换为没有单位的计数
"""


import re


def KMBConvert(value: str) -> int:
    pattern = r'(\d+\.?\d*)([KMB]?)'
    match = re.search(pattern, value)

    if match:
        number, suffix = match.groups()

        try:
            if suffix == 'K':
                return int(float(number) * 1000)
            elif suffix == 'M':
                return int(float(number) * 1000000)
            elif suffix == 'B':
                return int(float(number) * 1000000000)
            else:
                return int(float(number))
        except ValueError:
            return 0
    else:
        return 0