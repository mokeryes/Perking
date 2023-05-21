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
        while True:
            unique_ids = tiktok_explore(page=tiktok_page)
            print(unique_ids)

run()
