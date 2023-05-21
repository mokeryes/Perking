"""
一些工具函数
"""

import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), './'))

from load_cookies import load_cookies
from get_html import get_html
from email_operate import email_send, email_read
from loading_animation import start_loading_thread, stop_loading_thread

__version__ = '1.0.0'

__all__ = [
    'load_cookies',
    'get_html',
    'email_send', 'email_read',
    'start_loading_thread', 'stop_loading_thread'
]
