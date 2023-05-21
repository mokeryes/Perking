import json
import re
import json


def load_cookies(filename: str) -> dict:
    with open(filename, 'r') as f:
        content = f.read()

    content = re.sub(r'unspecified', 'Strict', content)
    content = re.sub(r'no_restriction', 'None', content)
    content = re.sub(r'lax', 'Lax', content)

    cookies = json.loads(content)

    return cookies

if __name__ == '__main__':
    cookies = load_cookies('./../../Resources/cookies/www.tiktok.com-lvthislv.cookies')
    print(cookies)
