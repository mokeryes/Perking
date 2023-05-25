from playwright.sync_api import sync_playwright, Page
from typing import Tuple
from time import sleep
from Common import *

from Common import *


def login_qingflow(page: Page) -> Page:
    """登录轻流工作台, 点击“新增建联”
    """
    username, password = '18397093021', '3021STOPs_'
    qingflow_login_url = 'https://accounts.qingflow.com/acc/passport/login'

    page.goto(qingflow_login_url)

    username_input = \
        'body > qf-root > qf-passport > div > ' + \
        'div.main-container.main-containe-right > div > qf-login > ' + \
        'div > div > form > nz-form-item:nth-child(1) > nz-form-control > ' + \
        'div > div > qf-user-name-input > div > nz-input-group > input'

    password_input = \
        'body > qf-root > qf-passport > div > div.main-container.main-containe-right > ' + \
        'div > qf-login > div > div > form > nz-form-item:nth-child(2) > ' + \
        'nz-form-control > div > div > nz-input-group > input'

    login_button = \
        'body > qf-root > qf-passport > div > ' + \
        'div.main-container.main-containe-right > div > qf-login > ' + \
        'div > div > nz-form-item > nz-form-control > div > div > button'

    page.get_by_text('账号密码登录').click()
    page.locator(selector=username_input).fill(username)
    page.locator(password_input).fill(password)
    page.locator(login_button).click()

    mine = \
        '#sidebar > qf-index-sidebar > div > div.sidebar-content > ' + \
        'div.custom-navigation-menu > qf-navigation > div > ' + \
        'div.scroll-wrapper > qf-scroll > overlay-scrollbars > ' + \
        'div.os-viewport.os-viewport-scrollbar-hidden > div > div:nth-child(3) > div'
    page.locator(mine).click()

    page.click('div.item-content')

    return page

def cancel_fill_data(page: Page):
    """
    取消建联, 关闭页面, 同时打开一个新的建联窗口
    """
    page.click('button.apply-operations-item:nth-of-type(2)')
    sleep(0.5)
    page.click('button[class="qf-btn qf-btn-danger"]')
    sleep(0.5)
    page.click('div.item-content')

def fill_data(page: Page, datas: dict) -> bool:
    """
    填充建联数据

    args:
        page: 已登录轻流的页面
        datas: 字典形式
            datas = {
                'basic': [Account, Followers, ChannelLink, Email],
                'ID': ID,
                'remarks': [remark1, remark2, ...],
                'email_screenshot': str,
                'REGION': str,
                'COUNTRY': str
            }
    return:
        如果录入成功则返回True
    """
    # 上传邮件截图
    page.get_by_role("button", name="拖拽或点击上传文件").locator("input[type=\"file\"]").set_input_files(datas['email_screenshot'])

    """
        nth0: Account (str)
        nth1: Followers (int)
        nth2: Channel Link (str)
        nth3: Email (str)
    """
    # 填入unique_id, chanel_link, email
    for nth, data in enumerate(datas['basic']):
        page.locator('input[placeholder="请输入内容"]').nth(nth).click()
        page.locator('input[placeholder="请输入内容"]').nth(nth).fill(data)

    # 选择Platform
    page.locator('qf-select[qfshowsearch=""]').nth(1).click() 
    if 'tiktok' in datas['basic'][2]:
        page.click('qf-option-item div.qf-select-item-option-content[title="Tiktok"]')
    elif 'Instagram' in datas['basic'][2]:
        page.click('qf-option-item div.qf-select-item-option-content[title="Instagram"]')
    elif 'youtube' in datas['basic'][2]:
        page.click('qf-option-item div.qf-select-item-option-content[title="Youtube"]')
    elif 'facebook' in datas['basic'][2]:
        page.click('qf-option-item div.qf-select-item-option-content[title="Facebook"]')
    elif 'Twitch' in datas['basic'][2]:
        page.click('qf-option-item div.qf-select-item-option-content[title="Twitch"]')
    else:
        print(f"未知平台: {datas['basic'][2]}")
        cancel_fill_data(page=page)
        return False

    # 选择region
    REGION = datas['REGION']
    page.locator('qf-select[qfshowsearch=""]').nth(2).click()
    page.click(f'qf-option-item div.qf-select-item-option-content[title="{REGION}"]')

    # 选择国家
    COUNTRY = datas['COUNTRY']
    page.locator('qf-select[qfshowsearch=""]').nth(3).click()
    # 多项选择框为动态加载，所以需要先滚动到最低下，才能获取全部的数据
    sleep(0.5)
    page.evaluate("document.querySelector('cdk-virtual-scroll-viewport').scrollBy(0, 200);")
    page.click(f'qf-option-item div.qf-select-item-option-content[title="{COUNTRY}"]')

    # 选择达人类型
    page.locator('qf-select[qfshowsearch=""]').nth(4).click()
    page.click(f'qf-option-item div.qf-select-item-option-content[title="DailyLife"]')

    user_type = ['lifestyle生活']
    checkbox_element = page.query_selector_all('span.radio-accessor-title')
    for t in user_type:
        for element in checkbox_element:
            if t in element.text_content():
                element.click()

    # 填写remarks
    remarks = ''
    for step, remark in enumerate(datas['remarks'], start=0):
        remarks += remark
        if step == 3:
            break
        else:
            remarks += ', '
    page.fill('div[class="form-control"] textarea[placeholder="请输入内容"]', remarks)

    # 如果是重复内容，则取消建联
    if '不允许重复内容' in page.content():
        cancel_fill_data(page=page)
        return False

    # 新的建联
    page.get_by_role("button", name="新的建联").click()

    # 再次申请
    page.click('button[qftype="primary"][class*="qf-btn"][class*="small"] >> span.ng-star-inserted:has-text("再次申请")')

    return True


if __name__ == '__main__':
    datas = {
        'basic': ['gnome', '32', 'https://www.tiktok.com/@gnome', 'gnome@gnome.com'],
        'ID': 'IT',
        'kol_type': 'DailyLife',
        'remarks': ['remark1', 'remark2']

    }
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        qingflow_page = context.new_page()

        qingflow_page = login_qingflow(page=qingflow_page)
        state, qingflow_page = fill_data(page=qingflow_page, data=datas)

        sleep(2000)
