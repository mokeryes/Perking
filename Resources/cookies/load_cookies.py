import json

with open('cn.noxinfluencer.com.cookies', 'r') as f:
    content = json.load(f)

cookies = {}
for cookie in content:
    cookies[cookie['name']] = cookie['value']

print(cookies)
