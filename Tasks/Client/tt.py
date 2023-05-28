#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-21 17:14:42
# @Description :  TikTok的建联任务
"""

import module_config
module_config.insert_path()

from playwright.sync_api import sync_playwright, Page
from typing import Tuple
import csv

from QingflowApi import *
from Common import *


def read_datas(filename: str) -> list:
    """
    从csv文件读取达人信息
    """
    users = []

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            unique_id = row[1]
            link = row[2]
            region = row[3]
            followers = str(row[4])[:-3]
            email = row[7]
            remarks = row[9][1:-1].replace("'", '').split(', ')

            users.append(
                {
                    'unique_id': unique_id,
                    'link': link,
                    'region': region,
                    'followers': followers,
                    'email': email,
                    'remarks': remarks
                }
            ) 

    return users

def email_content(email_config: dict, page: Page) -> Tuple[str, str]:
    """
    保存邮件截图

    args:
        email_config = {
            'template': str, # 邮件模板路径
            'content_path': str, # 邮件内容保存路径
            'pic_path': str, # 邮件截图保存路径
            'unique_id': str, # 用户unique_id
            'link': str, # 用户主页链接
            'email': str, # 用户邮箱地址
        }
        page (Page):
            用于截图的playwright Page对象

    returns:
        pic_path (str): 邮件截图路径, 用于上传到轻流
        content_path (str): 邮件内容路径, 用于邮件发送内容
    """

    with open(email_config['template'], 'r') as f:
        content = f.read()
    content = content.replace('XXX', email_config['link'])
    content = content.replace('kol', email_config['unique_id'])

    content_path = f"{email_config['content_path']}/{email_config['email']}.html"
    with open(content_path, 'w') as f:
        f.write(content)

    pic_path = f'{email_config["pic_path"]}/{email_config["email"]}.png'
    page.goto(f'file:///Users/mokerl/MokerProjects/Github/Perking/Tasks/Client/{content_path}')
    page.screenshot(path=pic_path)

    return (pic_path, content_path)

def tt_run():
    # 读取达人数据
    users = read_datas(filename='/Users/mokerl/Desktop/europe.csv')

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()

        qingflow_page = context.new_page()
        # 登录轻流
        qingflow_page = login_qingflow(page=qingflow_page)

        # 建联循环
        for user in users:
            # 判断用户是否为选中地区
            user_region = user['region']
            REGION = region(user_region)
            COUNTRY = country(user_region)
            if not REGION or not COUNTRY:
                print('未选中的地区')
                print(user)
                continue

            # 处理邮件信息（邮件内容以及截图）
            email_page = context.new_page()
            email_config = {
                'template': '../../Resources/email_template/temu_tiktok_email_template.html',
                'content_path': 'tt/content',
                'pic_path': 'tt/pic',
                'unique_id': user['unique_id'],
                'link': user['link'],
                'email': user['email']
            }
            pic_path, content_path = email_content(email_config=email_config, page=email_page)
            email_page.close()

            # 填入建联数据
            datas = {
                'basic': [user['unique_id'], user['followers'], user['link'], user['email']],
                'ID': user['region'],
                'remarks': user['remarks'],
                'email_screenshot': pic_path,
                'REGION': REGION,
                'COUNTRY': COUNTRY
            }
            status = fill_data(page=qingflow_page, datas=datas)
            
            # 如果建联成功，则发邮件，否则关闭建联页面
            if status:
                with open(content_path, 'r') as f:
                    content = f.read()

                email_info = {
                    'server': 'smtpdm.aliyun.com',
                    'port': 80,
                    'from_email': 'moker.lu@mails.perkinggroup.com',
                    'reply_to': 'moker.lu@perkinggroup.com',
                    'password': '3021MOKERperking',
                    'to_email': user['email'],
                    'cc_email': '',
                    'subject': \
                        "Partnership inquiry for TEMU app, Join TEMU's talent partner programme with 1000+ creators!",
                    'content': content
                }
                email_send(email_info=email_info)


tt_run()
