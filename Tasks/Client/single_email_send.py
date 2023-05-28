#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-28 19:04:24
# @Description : 使用邮件推送来发送单一邮件
"""


from module_config import insert_path
insert_path()

from Common import email_send


reply_to = 'xuan.qi@perkinggroup.com'
to_email = 'itsmelsommers@gmail.com'
cc_email = 'josh.ed@perkinggroup.com'
subject = 'TEMU ongoing cooperation with spoiledmel'
content = '''<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Cooperation Email</title>
</head>
<body>
	<p>Hi</p>
	<p>This is Xuan, Amber's manager, representing temu.</p>
	<p>We have an ongoing cooperation, but we never saw any reply from you since March.</p>
	<p>We'd like to move forward this cooperation so I EDITED THE VIDEO FOR YOU according to temu's feedback.</p>
	<p>Here is your video:</p>
	<p><a href="https://drive.google.com/file/d/1DKGnrlH89EnrjGNVzy-xNYGqoiNnZYQj/view?usp=share_link">https://drive.google.com/file/d/1DKGnrlH89EnrjGNVzy-xNYGqoiNnZYQj/view?usp=share_link</a></p>
	<p>All you need to do is JUST TO POST and add bio link and caption before May 31th, then you can EARN $800. We will arrange payment by bank transfer or PayPal after you up the video.</p>
	<p>Please tell me when you done.</p>
	<p>If you still don't reply us, we will kindly cancel this cooperation. Thanks.</p>
	<p>Caption: #nice temu##temu #code4code</p>
	<p>Click to get 90%off and 100 COUPON on Temu⬇️</p>
	<p><a href="https://temu.to/k/usbJkmLZIw6gzE5">https://temu.to/k/usbJkmLZIw6gzE5</a></p>
</body>
</html>
'''


email_info = {
    'server': 'smtpdm.aliyun.com',
    'port': 80,
    'from_email': 'moker.lu@mails.perkinggroup.com',
    'reply_to': reply_to,
    'password': '3021MOKERperking',
    'to_email': to_email,
    'cc_email': cc_email,
    'subject': subject,
    'content': content
}

email_send(email_info=email_info)