from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from time import sleep


def reach_qingflow():
    account = '18397093021'
    password = '3021STOPs_'
    url = 'https://qingflow.com/index/home'

    login_button_xpath = '/html/body/qf-root/qf-passport/div/div[1]/div/div/div'
    account_passwd_login_xpath = '/html/body/qf-root/qf-passport/div/div[1]/div/qf-login/div/div/nz-form-item/nz-form-control/div/div/div/a[1]'
    account_input_xpath = '/html/body/qf-root/qf-passport/div/div[1]/div/qf-login/div/div/form/nz-form-item[1]/nz-form-control/div/div/qf-user-name-input/div/nz-input-group[2]/input'
    passwd_input_xpath = '/html/body/qf-root/qf-passport/div/div[1]/div/qf-login/div/div/form/nz-form-item[2]/nz-form-control/div/div/nz-input-group/input'

    chrome = Chrome()
    chrome.set_window_size(width=1920, height=1080)

    chrome.get(url)

    try:
        chrome.find_element(by=By.XPATH, value=login_button_xpath).click()
    except:
        chrome.find_element(by=By.XPATH, value=account_passwd_login_xpath).click()
        chrome.find_element(by=By.XPATH, value=account_input_xpath).send_keys(account)
        chrome.find_element(by=By.XPATH, value=passwd_input_xpath).send_keys(password)

    sleep(2000)


if __name__ == '__main__':
    reach_qingflow()