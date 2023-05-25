import module_config
module_config.insert_path()

from playwright.sync_api import sync_playwright, Page
from bs4 import BeautifulSoup
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
        old_unique_ids = set()
        while True:
            unique_ids = tiktok_explore(page=tiktok_page)

            with open('tiktok_explore/UNIQUE_IDs.txt', '+a') as f:
                content = f.readlines()
            for item in content:
                unique_id = item[:-1]
                old_unique_ids.add(unique_id)
                print(unique_id)

            for unique_id in list(old_unique_ids):
                unique_ids.add(unique_id)

            with open('tiktok_explore/UNIQUE_IDs.txt', '+a') as f:
                for unique_id in list(unique_ids):
                    f.write(unique_id+'\n')

run()
