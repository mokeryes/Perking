#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 19:04:24
# @Description : 获取页面的html
"""


import requests
import json
import os
import logging

from time import sleep


def _get_cookies() -> dict:
    cookies = {}

    with open(f'../../Resources/cookies/www.tiktok.com-lvthislv.cookies', 'r') as f:
        content = json.load(f)

    for cookie in content:
        cookies[cookie['name']] = cookie['value']

    return cookies

def _get_headers() -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"
    }

    return headers

def get_html(url: str) -> str:
    logging.basicConfig(
        filename='./../Log/get_html.log',
        level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s'
    )

    logging.basicConfig(
        filename='./../Log/get_html.log',
        level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s'
    )

    if 'https://' not in url and 'http://' not in url:
        url = 'https://' + url

    platfrom = ''
    if 'tiktok' in url.lower():
        platfrom = 'tiktok'

    session = requests.session()

    headers = _get_headers()
    if 'tiktok' in url:
        cookies = _get_cookies()

    if cookies:
        session.cookies.update(cookies)

    for _ in range(3):
        try:
            print(f'[LOG] Connectting to {url}.')
            logging.info(f'[LOG] Connectting to {url}.')
            response = session.get(url=url, headers=headers, cookies=cookies, timeout=(10, 10))

            if response and len(response.text) > 4000:
                print(f'[LOG] Connection with {url} successful!')
                logging.info(f'[LOG] Connection with {url} successful!')
                return response.text

        except Exception as e:
            print(f'[ERROR] Connection error: {e}')
            logging.error(f'[ERROR] Connection error: {e}')
            sleep(2)

    session.close()

    return ''