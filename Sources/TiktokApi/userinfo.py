#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 19:04:24
# @Description : 获取 TikTok用户数据, 并解析返回
"""


import json
import logging
import re

from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime

from Common import get_html


class UserInfo:
    """
    region: get user region.
    time_list: get videos update list.
    follower_count: get user's follower count.
    heart_count: get user's heart count.
    median_view: get median view number for all videos.
    video_count: get user's video count.
    tags: get user's tags.
    biolink: get biolink from user's description.
    title: get user's title.
    email: get user's email.
    """
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, "html.parser")

        # HTML内容中的JSON转换为字典
        self.json_state = False
        try:
            json_data = self.soup.find("script", {"id": "SIGI_STATE"})
            self.data = json.loads(json_data.text)

            if json_data is None:
                logging.error("未从HTML中找到指定元素")
            else:
                self.json_state = True
                self.username = list(self.data.get('UserModule', {}).get('users', {}).keys())[0]

        except (AttributeError, json.JSONDecodeError) as e:
            logging.error(f"解析JSON数据时出现错误：{e}")

    def username(self) -> str:
        browser_username = self.soup.find_all('span', {'data-e2e': 'browse-username'})

        for username in browser_username:
            content = username.contents
            if len(content) > 1:
                username_text = content[0]
                verified_text = content[1].text.strip()
            else:
                username_text = content[0].strip()

        return username_text

    def nickname(self) -> str:
        browser_nickname = self.soup.find('span', {'data-e2e': 'browser-nickname'})
        nickname = browser_nickname.get_text().split(' · ')[0]
        print(f'nickname in userinfo class: {nickname}')

        return nickname

    def region(self) -> str:
        """
        获取Tiktok用户所处国家
        """
        region = ""

        if not self.json_state:
            return region

        video_id_list = list(self.data.get('ItemModule', []).keys())
        region_list = []
        for video_id in video_id_list:
            region_list.append(self.data.get('ItemModule', {}).get(video_id, {}).get('locationCreated'))

        if len(region_list) == 0:
            return ''

        counter = Counter(region_list)
        region = counter.most_common(1)[0][0]
    
        return region

    def time_list(self) -> list:
        if not self.json_state:
            return ""

        video_id_list = list(self.data.get('ItemModule', []).keys())
        time_list = []
        for video_id in video_id_list:
            time_list.append(self.data.get('ItemModule', {}).get(video_id, {}).get('createTime'))

        date_list = [datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S') for time in time_list]

        return date_list

    def follower_count(self) -> int:
        """
        获取Tiktok用户粉丝量
        """
        follower_count = 0

        if not self.json_state:
            return follower_count
        
        follower_count = self.data.get('UserModule', {}).get('stats', {}).get(self.username, {}).get('followerCount')

        return int(follower_count)

    def heart_counts(self) -> int:
        """
        获取Tiktok用户点赞量
        """
        heart_count = 0

        if not self.json_state:
            return heart_count
        
        heart_count = self.data.get('UserModule', {}).get('stats', {}).get(self.username, {}).get('heartCount')

        return int(heart_count)

    def median_view(self) -> int:
        """
        获取用户近期视频播放量中位数
        """
        if not self.json_state:
            return 0

        video_id_list = self.data.get("ItemModule", [])

        video_view_list = [video_data["stats"]["playCount"] for video_id, video_data in video_id_list.items()]
        if not video_view_list:
            return 0

        video_view_list.sort()
        n = len(video_view_list)
        if n % 2 == 0:
            return (video_view_list[n//2 - 1] + video_view_list[n//2]) // 2
        else:
            return video_view_list[n//2]

    def video_count(self) -> int:
        video_count = 0

        if not self.json_state:
            return video_count

        video_count = self.data.get('UserModule', {}).get('stats', {}).get(self.username, {}).get('videoCount')

        return video_count

    def tags(self) -> set():
        """
        获取用户视频类型
        """
        temp_list = []
        type_list = []

        if not self.json_state:
            return set()

        item_module = self.data.get("ItemModule", {})
        for item in item_module.values():
            labels = item.get("diversificationLabels", [])
            for label in labels:
                temp_list.append(label)

        # 寻找出现次数最多的四个tag
        counter = Counter(temp_list)
        most_common = counter.most_common(5)

        for item in most_common:
            type_list.append(item[0])

        return list(type_list)

    def biolink(self) -> str:
        """
        获取主页个人简介的外链
        """
        biolink = ''

        if not self.json_state:
            return ''

        biolink = self.data.get('UserModule', {}).get('users', {}).get(self.username, {}).get('bioLink', {}).get('link')

        return biolink

    def title(self) -> str:
        title = ''

        if not self.json_state:
            return title

        title = self.data.get('SEOState', {}).get('metaParams', {}).get('title')

        return title

    def email(self, MCN: bool):
        """
        获取Tiktok用户Email
        """
        if not self.json_state:
            return ""

        pattern = r"\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}"

        email_providers = {
            "gmail.com",
            "icloud.com",
            "outlook.com",
            "yahoo.com",
            "hotmail.com"
        }

        # Get email from bio message.
        description = self.data.get('SEOState', {}).get('metaParams', {}).get('description', "")
        email = re.findall(pattern, description)
        if email:
            email = email[0]
            if not MCN and email.split("@")[1].lower() not in email_providers:
                email = ""
            return email

        # Get email from biolink.
        biolink = self.biolink()
        
        if not biolink:
            return ""

        html = get_html(url=self.biolink())
        soup = BeautifulSoup(html, 'html.parser')

        # if mailto exist
        for link in soup.find_all('a'):
            if link.has_attr('href'):
                if re.match("mailto:", link['href']):
                    email = link['href'][7:]
                    if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
                        if not MCN and email.split("@")[1].lower() not in email_providers:
                            email = ""
                        return email

        # else re
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_list = re.findall(pattern, html)
        if email_list:
            email_list = set(email_list)
            for email in email_list:
                if email.split("@")[1].lower() in email_providers:
                    return email
        return ""



if __name__ == "__main__":
    with open('elsalout.html', 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    try:
        user = UserInfo(html=html)

        video_type = user.tags()
        region = user.region()
        link = user.biolink()
        median_view = user.median_view()
        email = user.email(MCN=False)
        follower_count = user.follower_count()
        title = user.title()
        createTime = user.time_list()

        print(f"biolink: {link}")
        print(f"video type: {video_type}")
        print(f"region: {region}")
        print(f'median view: {median_view}')
        print(f'email: {email}')
        print(f'follower count: {follower_count}')
        print(f'title: {title}')

    except FileNotFoundError as e:
        print(f"无html文件: {e}")
