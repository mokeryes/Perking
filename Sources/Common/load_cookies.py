#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 19:04:24
# @Description : 从文件读取cookies并返回
"""


import json
import re


def load_cookies(filename: str) -> dict:
    with open(filename, 'r') as f:
        content = f.read()

    content = re.sub(r'unspecified', 'Strict', content)
    content = re.sub(r'no_restriction', 'None', content)
    content = re.sub(r'lax', 'Lax', content)

    cookies = json.loads(content)

    return cookies

if __name__ == '__main__':
    cookies = load_cookies('./../../Resources/cookies/www.tiktok.com-lvthislv.cookies')
    print(cookies)
