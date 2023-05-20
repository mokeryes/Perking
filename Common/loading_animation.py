'''
邮件发送
'''

import sys
import threading
import time


def _loading(title: str):
    print(title)

    chars = [' ─── ', '  \\  ', '  |  ', '  /  ']

    while not threading.current_thread().stopped:
        for char in chars:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b\b\b\b\b')

def start_loading_thread(title: str):
    thread = threading.Thread(target=_loading, args=(title,))
    thread.stopped = False
    thread.start()

    return thread

def stop_loading_thread(thread: threading.Thread):
    thread.stopped = True
    thread.join()

    sys.stdout.write('\x1b[2K')  # 清空当前行的内容
    sys.stdout.write('\r')      # 将光标移动到行首
    sys.stdout.flush()


if __name__ == '__main__':
    loading_thread = start_loading_thread(title='loading') 

    print('Some operations are working...', end='\t')
    time.sleep(3)

    stop_loading_thread(thread=loading_thread)
