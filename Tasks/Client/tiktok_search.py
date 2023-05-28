#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-14 03:35:31
# @Description : 从TikTok搜索用户
"""


from playwright.sync_api import sync_playwright, Page
from time import sleep

from Common import *
from NoxApi import *
from TiktokApi import *


def nox_handle(page: Page) -> list:
    return nox_run(page=page)

def tiktok_handle(page: Page, keyword: str) -> list:
    page = tiktok_search(page=page, keyword=keyword)

    search_user_info_container_head = '#tabs-0-panel-search_top > div > div > div:nth-child('
    search_user_info_container_nth: int
    search_user_info_container_tail = ') > div.tiktok-1d5vh4i-DivLink.e10wilco0'

    search_card_user_unique_id_head = '#search_top-item-user-link-'
    search_card_user_unique_id_nth: int
    search_card_user_unique_id_tail = ' > div > p'

    user_unique_ids = set()

    while True:
        prev_page = rolling_page_down(page=page)
        for _ in range(12):
            page = rolling_page_down(page=page)
        if prev_page == page:
            break

    for search_card_user_unique_id_nth in range(1000):
        try:
            # rolling_page_down(page=page)

            user_unique_id = page.locator(
                search_card_user_unique_id_head + \
                str(search_card_user_unique_id_nth) + \
                search_card_user_unique_id_tail
            ).inner_html(timeout=5000)

            if user_unique_id not in user_unique_ids:
                user_unique_ids.add(user_unique_id)
                print(user_unique_id, end='\t')

        except Exception as e:
            # 页面滚动到最底部后break
            print(e)
            break

    with open('tiktok_search/searched_users.txt', '+a') as f:
        file_content = f.readlines()

        for user_unique_id in list(user_unique_ids):
            if user_unique_id not in file_content:
                f.write(user_unique_id + '\n')

    return list(user_unique_ids)

def run():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        # nox_page = context.new_page()

        # nox handle
        # nicknames = nox_handle(page=nox_page)
        # nox_page.close()
        keywords_1 = [
             'tech review', 'tech gadgets',
             'tech accessories', 'tech news', 'tech tips', 'tech hacks', 'smart home',
             'smart devices', 'AI technology', 'virtual reality', 'augmented reality',
             '3D printing', 'drones', 'robotics', 'programming', 'coding', 'software development', 
             'web development', 'graphic design', 'video editing', 'photography', 'vlogging', 
             'influencer', 'content creator'
        ]
        keywords_2 = ['wearable technology', 'fitness tracker', 'smartwatch', 'smart glasses', 'virtual assistant', 'wireless charger', 'power bank', 'USB hub', 'external hard drive', 'memory card', 'printer', 'monitor', 'keyboard', 'mouse', 'webcam', 'microphone', 'speaker', 'smart speaker', 'voice assistant', 'home assistant', 'smart lock', 'security camera', 'alarm system', 'thermostat', 'smart thermostat', 'electric vehicle', 'electric car', 'hybrid car', 'solar panel', 'smart home technology', 'home automation', 'smart lighting', 'LED lighting', 'smart TV', 'streaming device', 'media player', 'virtual keyboard', 'wireless headphones', 'Bluetooth headset', 'noise-cancelling headphones', 'gaming chair', 'ergonomic chair', 'standing desk', 'ergonomic desk', 'VR headset', 'AR headset', 'smart scale', 'smart mirror', 'smart kitchen', 'smart appliances', 'smart coffee maker', 'smart refrigerator', 'smart oven', 'smart microwave', 'smart blender', 'smart water bottle', 'smart thermostat', 'smart air purifier', 'smart humidifier', 'smart vacuum cleaner', 'smart lawn mower', 'smart bike', 'smart home security', 'smart doorbell', 'smart garage door opener', 'smart smoke detector', 'smart carbon monoxide detector', 'smart water leak detector', 'smart sprinkler system', 'smart pet feeder', 'smart pet door', 'smart baby monitor', 'smart bed', 'smart pillow', 'smart lighting control', 'smart thermostat control', 'smart home hub', 'smart remote control', 'smart plug', 'smart switch', 'smart outlet', 'smart door lock', 'smart window shades', 'smart blinds', 'smart garden', 'smart plant pot', 'smart irrigation system', 'smart pool', 'smart shower', 'smart toothbrush', 'smart skincare', 'smart hair care', 'smart hairbrush', 'smart mirror', 'smart fashion', 'smart clothing', 'smart jewelry', 'smart backpack', 'smart luggage', 'smart bike lock', 'smart bike helmet', 'smart wallet', 'smart credit card', 'smart glasses', 'smart contact lens', 'smart ring', 'smart tattoo', 'smart home insurance', 'smart city', 'smart grid', 'smart building', 'smart office', 'smart factory', 'smart agriculture', 'smart transportation', 'smart logistics', 'smart waste management', 'smart recycling', 'smart healthcare', 'smart hospital', 'smart medicine', 'smart pharmacy', 'smart fitness', 'smart sports', 'smart coaching', 'smart nutrition', 'smart wellness', 'smart beauty', 'smart aging', 'smart sleep', 'smart education', 'smart learning', 'smart e-learning', 'smart school', 'smart campus', 'smart library', 'smart museum', 'smart tourism', 'smart city tourism', 'smart travel', 'smart hotel', 'smart hospitality', 'smart restaurant', 'smart food', 'smart agriculture', 'smart farming', 'smart forestry', 'smart fishing', 'smart mining', 'smart energy', 'smart power', 'smart grid', 'smart home energy management', 'smart meter', 'smart city energy', 'smart water', 'smart waste', 'smart recycling', 'smart green', 'smart sustainability']
        nicknames = keywords_1 + keywords_2

        # tiktok handle
        tiktok_page = context.new_page()
        tiktok_page.set_default_navigation_timeout(5*60*1000)
        tiktok_page = login_tiktok(page=tiktok_page)

        for nickname in nicknames:
            tiktok_handle(page=tiktok_page, keyword=nickname)
            sleep(3)
        tiktok_page.close()

        sleep(2000)


if __name__ == '__main__':
    run()
