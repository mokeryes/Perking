#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-18 07:17:26
# @Description : 
"""

import pandas as pd

from common import *


def xlsx_data(filename: str):
    df = pd.read_excel(filename, sheet_name='Sheet1')
    users_data = []

    for _, row in df.iterrows():
        username = row[0]
        link = row[1]
        email = row[2]

        if '@' not in email:
            continue

        users_data.append(
            {
                'username': username,
                'link': link,
                'email': email
            }
        )

    for item in users_data:
        print(item)

    return users_data

users_data = xlsx_data(filename='/Users/mokerl/Desktop/seeding.xlsx')

for user_data in users_data:
    with open('Resources/email_template/for_temu_instagram.html', 'r') as f:
        content = f.read().replace('LINK', user_data['link'])
        content = content.replace('KOL', user_data['username'])

    email_info = {
        'server': 'smtpdm.aliyun.com',
        'port': 80,
        'from_email': 'moker.lu@mails.perkinggroup.com',
        'reply_to': 'summer.he@perkinggroup.com',
        'password': '3021MOKERperking',
        'to_email': user_data['email'],
        'subject': \
            "Partnership inquiry for TEMU app, Join TEMU's talent partner programme with 1000+ creators!",
        'content': content
    }

    with open(f'/Users/mokerl/Desktop/email_sent_log/{user_data["email"]}.html', 'w') as f:
        f.write(content)

    email_send(email_info=email_info)
