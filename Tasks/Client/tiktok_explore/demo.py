#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 22:48:38
# @Description : 
"""

with open('uniqueids.txt', 'r') as f:
    unique_ids = [line.strip() for line in f.readlines()]

print(len(unique_ids))
print(len(set(unique_ids)))
