#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 19:04:24
# @Description : 探索TikTok并获取用户
"""


import module_config
module_config.insert_path()

from playwright.sync_api import sync_playwright
from time import sleep

from Common import *
from TiktokApi import *


def run():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        tiktok_page = context.new_page()
        tiktok_page.set_default_navigation_timeout(5*60*1000)

        tiktok_page = login_tiktok(page=tiktok_page)

        unique_ids = set()
        while True:
            try:
                unique_ids = tiktok_explore(page=tiktok_page)
            except:
                sleep(5)
                continue

            # 读取
            with open('tiktok_explore/UNIQUE_IDs.txt', 'r') as f:
                old_users = [line.strip() for line in f.readlines()]
            users = set(old_users)
            
            # 添加
            for user in unique_ids:
                users.add(user)

            # 重新写入
            with open('tiktok_explore/UNIQUE_IDs.txt', 'w') as f:
                for user in list(users):
                    f.write(user+'\n')

            print(f'[{len(users)}]')

run()
