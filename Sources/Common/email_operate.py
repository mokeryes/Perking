#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 19:04:24
# @Description : 读取邮箱, 发送邮件
"""


import smtplib
import imaplib
import email
import email.header
import email.utils

from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rich.progress import track
from rich.table import Table
from rich.console import Console
from rich import print as rprint
from terminaltables import SingleTable

from Common.loading_animation import start_loading_thread, stop_loading_thread


def _decode(content) -> str:
    decoded_content = ''

    try:
        parts = email.header.decode_header(content)
    except Exception as e:
        print(e)
        return content

    for part in parts:
        charset = part[1]
        encoded_string = part[0]

        if isinstance(encoded_string, bytes) and charset:
            decoded_string = encoded_string.decode(charset)
        else:
            if "b' " in str(encoded_string):
                encoded_string = ' ' + str(encoded_string)[3:-1]
            elif "b'" in str(encoded_string):
                encoded_string = ' ' + str(encoded_string)[2:-1]
            decoded_string = encoded_string

        decoded_content += decoded_string

    return decoded_content


def email_send(email_info: dict):
    '''
    email_info = {
        'server': str,      # 发件服务器
        'port': int,        # 发件服务器端口
        'from_email': str,  # 发件箱，统一为 moker.lu@mails.perkinggroup.com
        'reply_to': str,    # 收件箱，可以任意设置，邮件推送出去之后对方回复信件的目标邮箱
        'password': str     # moker.lu@mails.perkinggroup.com 推送邮箱的密码
        'to_email': str,    # 邮件的目标邮箱, 也就是不同kol的邮箱
        'cc_email': str,    # 设置抄送邮箱
        'subject': str,     # 邮件主题
        'content': str      # 邮件内容
    }
    '''
    server = email_info['server']
    port = email_info['port']
    from_email = email_info['from_email']
    reply_to = email_info['reply_to']
    password = email_info['password']
    to_email = email_info['to_email']
    cc_email = email_info['cc_email']
    subject = email_info['subject']
    content = email_info['content']

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Cc'] = cc_email
    msg['Reply-to'] = reply_to
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html'))

    table = Table(title='发件内容')
    console = Console()

    table.add_column('邮件信息', style='cyan', justify='left', no_wrap=False)

    table.add_row('Subject: ' + msg['Subject'])
    table.add_row(msg['From'] + ' -> ' + msg['To'])
    table.add_row('Reply to: ' +  msg['Reply-to'])

    console.print(table, justify='left')
    
    try:
        rprint(f'正在连接服务器：[bold yellow]Server: {server}, Port: {port}[/bold yellow]')
        sleep(0.5)
        if port == 465:
            smtp_conn = smtplib.SMTP_SSL(server, port)
            print('SSL加密发送.')
        elif port == 25:
            smtp_conn = smtplib.SMTP(server, port)
            print('非SSL加密发送.')
        elif port == 80:
            print('非SSL加密推送邮件.')
            smtp_conn = smtplib.SMTP(server, port)
        else:
            rprint(f'[bold red]端口错误，端口：{port}.[/bold red]')
            exit(1)

        rprint(f'正在登录：[bold yellow]Username: {from_email}[/bold yellow]')
        smtp_conn.login(from_email, password)
        sleep(0.5)

        print(f'正在发送邮件：{from_email} -> {to_email}')
        if cc_email:
            smtp_conn.sendmail(from_email, [to_email] + [cc_email], msg.as_string())
        else:
            smtp_conn.sendmail(from_email, [to_email], msg.as_string())
        smtp_conn.quit()
        sleep(0.5)

        rprint(f'[bold green]邮件发送成功：{from_email} -> a{to_email}[/bold green]')

    except smtplib.SMTPConnectError as e:
        rprint(f'[bold red]邮件发送失败，连接失败： {e.smtp_code, e.smtp_error}[/bold red]')
    except smtplib.SMTPAuthenticationError as e:
        rprint(f'[bold red]邮件发送失败，认证错误： {e.smtp_code, e.smtp_error}[/bold red]')
    except smtplib.SMTPSenderRefused as e:
        rprint(f'[bold red]邮件发送失败，发件人被拒绝： {e.smtp_code, e.smtp_error}[/bold red]')
    except smtplib.SMTPRecipientsRefused as e:
        rprint(f'[bold red]邮件发送失败，收件人被拒绝： {e}[/bold red]')
    except smtplib.SMTPDataError as e:
        rprint(f'[bold red]邮件发送失败，数据接收拒绝： {e.smtp_code, e.smtp_error}[/bold red]')
    except smtplib.SMTPException as e:
        rprint(f'[bold red]邮件发送失败, {e.message}[/bold red]')
    except Exception as e:
        rprint(f'[bold red]邮件发送异常, {str(e)}[/bold red]')

def email_read(email_info: dict) -> list:
    '''
    email_info = {
        'server': str,
        'port': int,
        'from_email': str,
        'password': str,
        'state': str,
        'keywords': str,
        'start_date': str,
        'end_date': str
    }
    '''
    server = email_info['server']
    port = email_info['port']
    from_email = email_info['from_email']
    password = email_info['password']

    loading_thread = start_loading_thread(title=f'正在连接服务器：Server: {server}, Port: {port}')
    if port == 143:
        imap = imaplib.IMAP4(server, port)
    elif port == 993:
        iamp = imaplib.IMAP4_SSL(server, port)
    else:
        print('收件服务器端口配置错误.')
        exit(1)
    stop_loading_thread(thread=loading_thread)

    loading_thread = start_loading_thread(title=f'正在登录：Username: {from_email}')
    imap.login(from_email, password)
    imap.select('INBOX')
    stop_loading_thread(thread=loading_thread)

    loading_thread = start_loading_thread(title=f'正在检索邮件：Username: {from_email}')
    status, messages = imap.search(None, 'ALL')
    messages = messages[0].split(b' ')[::-1]
    stop_loading_thread(thread=loading_thread)

    email_content_list = []

    for step, message in zip(track(range(len(messages))), messages):
        _, msg_data = imap.fetch(message, '(FLAGS RFC822)')
        flags = msg_data[0]
        email_msg = email.message_from_bytes(msg_data[0][1])

        subject = _decode(content=email_msg['Subject'])
        sender = _decode(email_msg['From'])
        receiver = _decode(email_msg['To'])

        if email_msg['Date']:
            datetime = str(email.utils.parsedate_to_datetime(email_msg['Date']))
        else:
            datetime = 'None'
        content = ''

        for part in email_msg.walk():
            if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                if part.get_content_charset():
                    content = str(part.get_payload(decode=True), part.get_content_charset())
                else:
                    content = str(part.get_payload(decode=True))
        data = [
            ['Content', content],
            ['Subject', subject],
            ['Sender', sender],
            ['Receiver', receiver],
            ['datetime', datetime]
        ]

        if 'Long-lasting' not in content:
            continue

        table = Table(title='邮件信息')
        console = Console()

        table.add_column('邮件信息', style='cyan', justify='left', no_wrap=False)
        table.add_column('邮件内容', style='magenta')

        for item in data:
            table.add_row(item[1])

        try:
            console.print(table, justify='left')
        except:
            singletable = SingleTable(data)
            print(singletable.table)
        console.print(f"[{step+1}/{len(messages)}]")

        sleep(0.5) # Waitting for a prefect progress bar.

    imap.close()
    imap.logout()


    return email_content_list 

def _test_send():
    with open('../Resources/email_template/temu_tiktok_email_template.html', 'r') as f:
        content = f.read().replace('LINK', 'https://www.tiktok.com/@moker')
        content = content.replace('KOL', 'moker')

    email_info = {
        'server': 'smtpdm.aliyun.com',
        'port': 80,
        'from_email': 'moker.lu@mails.perkinggroup.com',
        'reply_to': 'moker.lu@perkinggroup.com',
        'password': '3021MOKERperking',
        'to_email': 'lvthislv@gmail.com',
        'subject': '测试邮件',
        'content': content
    }

    email_send(email_info=email_info)

def _test_read():
    email_info = {
        'server': 'imap.qiye.aliyun.com',
        'port': 143,
        'from_email': 'moker.lu@perkinggroup.com',
        'password': '3021STOPs_'
    }

    email_read(email_info=email_info, state='ALL')

if __name__ == '__main__':
    # _test_send()
    _test_read()
