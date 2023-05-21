#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-18 07:17:26
# @Description : 
"""

import pandas as pd

from Common import *


def xlsx_data(filename: str):
    df = pd.read_excel(filename, sheet_name='userlist')
    users_data = []

    for _, row in df.iterrows():
        username = row[1]
        link = row[4]
        email = row[7]

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

users_data = xlsx_data(filename='/Users/mokerl/Desktop/kols.xlsx')

for user_data in users_data:
    with open('Resources/email_template/temu_tiktok_email_template.html', 'r') as f:
        content = f.read().replace('XXX', user_data['link'])
        content = content.replace('kol', user_data['username'])

    email_info = {
        'server': 'smtpdm.aliyun.com',
        'port': 80,
        'from_email': 'moker.lu@mails.perkinggroup.com',
        'reply_to': 'moker.lu@perkinggroup.com',
        'password': '3021MOKERperking',
        'to_email': user_data['email'],
        'subject': \
            "Partnership inquiry for TEMU app, Join TEMU's talent partner programme with 1000+ creators!",
        'content': content
    }

    with open(f'/Users/mokerl/Desktop/email_sent_log/{user_data["email"]}.html', 'w') as f:
        f.write(content)

    # email_send(email_info=email_info)
