#!/usr/bin/env python3

import re

from bs4 import BeautifulSoup
from playwright.sync_api import Page
from time import sleep


def login_nox(page: Page):
    url = 'https://cn.noxinfluencer.com/search/tiktok/channel'

    page.goto(url)

    # Loginning
    account = '742851608@qq.com'
    password = 'Perkin2103'

    login_button_xpath = 'xpath=' + \
        '//*[@id="__layout"]/div/section/section/main/div/div[2]/div/div[2]/div[1]/div/div[1]/a'
    account_input_xpath = 'xpath=' + \
        '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[3]/form/div[1]/div/div/div[1]/input'
    password_input_xpath = 'xpath=' + \
        '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[3]/form/div[2]/div/div/div/input'
    logining_button_xpath = 'xpath=' + \
        '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[3]/form/div[4]/div/div'

    page.locator(login_button_xpath).click()
    page.locator(account_input_xpath).fill(account)
    page.locator(password_input_xpath).fill(password)
    page.locator(logining_button_xpath).click()

    while True:
        status = input('Ready to collect users?(y/n)')
        if status == 'y':
            return page
        else:
            continue

def fetch_users(page: Page):
    soup = BeautifulSoup(page.content(), 'html.parser')
    nickname_as = soup.find_all('a', {'class': 'title ellipsis'})
    nickname_list = []

    for nickname_a in nickname_as:
        nickname_a_str = str(nickname_a)
        nickname_a_str = re.sub(r'\n', '', nickname_a_str)
        nickname = re.findall(r'<a.*?>(.*?)</a>', nickname_a_str)
        nickname_list.append(nickname[0].strip())

    return nickname_list

def page_update(page: Page):
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    # next_page_xpath = \
        # '//*[@id="__layout"]/div/section/section/main/div/div[3]/div/div[2]/div[1]/div/div/div/div[3]/div[2]/div[6]'
    # page.locator(next_page_xpath).click()
    return page

def nox_run(page: Page):
    page = login_nox(page=page)
    nicknames = []

    while True:
        nickname_list = fetch_users(page=page)
        print(nickname_list)
        for nickname in nickname_list:
            nicknames.append(nickname)

        state = input('Ready for update page now?(y/n)')
        if state == 'y':
            page = page_update(page=page)
            sleep(1)
            continue
        else:
            break

    page.close()

    return nicknames


if __name__ == '__main__':
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_navigation_timeout(timeout=5*60*1000)

        print(nox_run(page=page))
