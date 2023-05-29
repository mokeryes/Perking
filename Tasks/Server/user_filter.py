#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 19:16:21
# @Description : 
"""


from module_config import insert_path
insert_path()

import os
import csv
import logging

from random import choice
from datetime import datetime, timedelta

from TiktokApi import UserInfo
from Common import KMBConvert, get_html


ROLE = {
    "FRBEGIN": "20K",
    "FREND": "20M",
    "HTMIN": "6K",
    "VRMIN": "6K",
}

logging.basicConfig(
    filename="../../Logs/user_filter.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def read_users(usersfile: str) -> set:
    with open('user_filter/MATCHED.txt', 'r') as f:
        old_users = [line.strip() for line in f.readlines()]
    
    new_users = set(old_users)
    if len(new_users) < len(old_users):
        with open('user_filter/UNMATCH.txt', 'w') as f:
            for new_user in list(new_users):
                f.write(new_user+'\n')

    return set(new_users)

def user_update(unique_id: str):
    unmatch_users = read_users(usersfile='user_filter/UNMATCH.txt')

    with open('user_filter/MATCHED.txt', '+a') as f:
        f.write(unique_id+'\n')

    with open('user_filter/UNMATCH.txt', 'w') as f:
        for user in list(unmatch_users):
            if user != unique_id:
                f.write(user+'\n')

def match_user(username: str, role: dict) -> bool:
    for _ in range(3):
        html = get_html(url='https://www.tiktok.com/@'+username)

        if not html:
            return False

        user = UserInfo(html=html)
        if user.json_state:
            break

    now = datetime.now()
    time_difference = timedelta(hours=8)
    new_time = now + time_difference
    formatted_time = new_time.strftime("%Y-%m-%d %H:%M:%S")

    region = user.region()
    email = user.email(MCN=False)
    biolink = user.biolink()
    follower_count = user.follower_count()
    heart_count = user.heart_counts()
    median_view = user.median_view()
    tags = user.tags()

    print(
        f'update: {formatted_time}\n',
        f'username: {username}\n',
        f'email: {email}\n',
        f'region: {region}\n',
        f'biolink: {biolink}\n',
        f'follower count: {follower_count}\n',
        f'heart count: {heart_count}\n',
        f'median view: {median_view}\n',
        f'tags: {tags}'
    )

    user_valid = True

    if not (KMBConvert(ROLE["FRBEGIN"]) < follower_count < KMBConvert(ROLE["FREND"])):
        return False

    if not email:
        return False

    if not (KMBConvert(ROLE["HTMIN"]) < heart_count):
        return False

    if not (KMBConvert(ROLE["VRMIN"]) < median_view):
        return False

    if user_valid:
        user_data = [
            formatted_time,
            username,
            'https://www.tiktok.com/@'+username,
            region,
            follower_count,
            heart_count,
            median_view,
            email,
            biolink,
            tags
        ]
        with open('user_filter/userlist.csv', mode='a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(user_data)

    logging.info(f"\n \
                   \tupdate: {formatted_time}\n \
                   \tusername: {username}\n \
                   \tregion: {region}\n \
                   \temail: {email}\n \
                   \tfollower_count: {follower_count}\n \
                   \theart_count: {heart_count}\n \
                   \tmedian view: {median_view}\n \
                   \tbiolink: {biolink}")

    return user_valid


def main(role: dict):
    if not os.path.exists('user_filter/userlist.csv'):
        with open('user_filter/userlist.csv', mode='a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['update', 'username', 'link', 'region', 'followers',
                 'heart', 'median_view', 'email', 'biolink', 'tags']
            )

    # match 之前首先去除与 MATCHED.txt 中重复的数据
    unmatch_users = read_users(usersfile='user_filter/UNMATCH.txt')
    matched_users = read_users(usersfile='user_filter/MATCHED.txt')
    new_unmatch_users = unmatch_users - matched_users
    with open('user_filter/UNMATCH.txt', 'w') as f:
        for user in list(new_unmatch_users):
            f.write(user+'\n')

    current_count = 0
    while True:
        # 用户重复检查
        unmatch_users = read_users(usersfile='user_filter/UNMATCH.txt')
        matched_users = read_users(usersfile='user_filter/MATCHED.txt')

        user_list = unmatch_users - matched_users
        if not user_list:
            print("用户数据枯竭，请重新做种")
            with open('user_filter/userlist.csv', '+a') as f:
                writer = csv.writer(f)
                writer.writerow(f'Done: {current_count}')
            break

        tiktokuser = choice(list(user_list))
        user_update(unique_id=tiktokuser)

        # 开始match
        if match_user(username=tiktokuser, role=ROLE):
            current_count += 1

        print(f"[{current_count}]")


main(role=ROLE)