#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-21 19:38:50
# @Description : 通过国家简称来获取国家名与大洲
"""


ID_COUNTRY = {
    # Europe
    'GB': 'UK',
    'FR': 'France',
    'DE': 'Germany',
    'IT': 'Italy',
    'ES': 'Spain',

    # NA
    'US': 'USA',
    'CA': 'Canada',

    # Pacific
    'NZ': 'NewZealand',
    'AU': 'Australia'
}

REGION_ID = {
    'Europe': [
        'GB',
        'FR',
        'DE',
        'IT',
        'ES',
    ],

    'NA': [
        'US',
        'CA'
    ],

    'Pacific': [
        'NZ',
        'AU'
    ]
}

def region(ID: str) -> str:
    """
    获取国家所属大洲
    """
    for region, _id in REGION_ID.items():
        if ID in _id:
            return region
    return ''

def country(ID: str) -> str:
    """
    获取国家名
    """
    return ID_COUNTRY.get(ID)


if __name__ == '__main__':
    ID = 'GB'

    print(region(ID=ID))
    print(country(ID=ID))

    if not region(ID=ID):
        print('not region')
    if not country(ID=ID):
        print('not country')
