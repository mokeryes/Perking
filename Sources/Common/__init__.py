"""
一些工具函数
"""


from Common.load_cookies import load_cookies
from Common.get_html import get_html
from Common.email_operate import email_send, email_read
from Common.loading_animation import start_loading_thread, stop_loading_thread
from Common.location import region, country

__version__ = '1.0.0'

__all__ = [
    'load_cookies',
    'get_html',
    'email_send', 'email_read',
    'start_loading_thread', 'stop_loading_thread',
    'region', 'country'
]
