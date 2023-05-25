from bs4 import BeautifulSoup
from playwright.sync_api import Page
from time import sleep

from Common.load_cookies import load_cookies


def login_tiktok(page: Page) -> Page:
    """login tiktok home page using chrome.

    args:
        page (Page): brand new page for tiktok.
    returns:
        page (Page): return loginned page.
    """
    url = 'https://www.tiktok.com'

    page.context.add_cookies(load_cookies(
        '../../Resources/cookies/www.tiktok.com-mokerorg.cookies'
        )
    )

    page.goto(url=url)

    return page

def tiktok_search(page: Page, keyword: str) -> Page:
    """searching for given keyword.

    args:
        page (Page): loginned page.
        nickname (str): nickname for tiktok user.
    return:
        page (Page): searched page.
    """
    search_user_input = page.locator(
        "#app > " + \
        "div.tiktok-xk7ai4-DivHeaderContainer.e10win0d0 > " + \
        "div > " + \
        "div.tiktok-1h3oqen-DivHeaderCenterContainer.e15qqn8h0 > " + \
        "div > " + \
        "form > " + \
        "input"
    )
    search_user_input.click()
    search_user_input.fill(keyword)

    search_user_button = page.locator(
        "#app > " + \
        "div.tiktok-xk7ai4-DivHeaderContainer.e10win0d0 > " + \
        "div > " + \
        "div.tiktok-1h3oqen-DivHeaderCenterContainer.e15qqn8h0 > " + \
        "div > " + \
        "form > " + \
        "button"
    )
    search_user_button.click()

    return page

def _tiktok_explore_page_unique_ids(page: Page) -> list:
    """fetch user unique id from tiktok exploring page.
    """
    user_container = \
        '#main-content-explore_page > ' + \
        'div > ' + \
        'div.tiktok-1qb12g8-DivThreeColumnContainer.eegew6e2 > ' + \
        'div'
    container_html: str
    container_html_length = 0

    while True:
        rolling_page_down(page=page)

        container_html = page.locator(user_container).inner_html()
        if len(container_html) == container_html_length:
            rolling_page_top(page=page)
            break
        else:
            container_html_length = len(container_html)

    unique_ids_soup = BeautifulSoup(container_html, 'html.parser')
    unique_ids_soups = unique_ids_soup.find_all('p', {'data-e2e': 'explore-card-user-unique-id'})

    unique_ids = []

    for soup in unique_ids_soups:
        soup = BeautifulSoup(str(soup), 'html.parser')
        unique_id = soup.find('p', {'data-e2e': 'explore-card-user-unique-id'}).getText()
        unique_ids.append(unique_id)
        print(unique_id)

    return unique_ids

def tiktok_explore(page: Page) -> list:
    """get unique id from explore page.

        return: a list for unique id.
    """
    page.goto('https://www.tiktok.com/explore')

    mode_container = \
        '#main-content-explore_page > ' + \
        'div > ' + \
        'div.tiktok-5xaaoq-DivCategoryListWrapper.e13i6o240 > ' + \
        'div.tiktok-1mdrotr-DivCategoryListContainer.e13i6o241'
    modes = page.inner_text(mode_container).split('\n')
    print(modes)

    other_mode_head = \
        '#main-content-explore_page > ' + \
        'div > ' + \
        'div.tiktok-5xaaoq-DivCategoryListWrapper.e13i6o240 > ' + \
        'div.tiktok-1mdrotr-DivCategoryListContainer.e13i6o241 > ' + \
        'div:nth-child('
    other_mode_nth: int
    other_mode_tail = ')'

    print(f'Exploring "{modes[0]}" now.')
    _tiktok_explore_page_unique_ids(page=page)

    modes = modes[1:]
    unique_ids = set()

    for mode_count, mode in enumerate(modes, start=2):
        other_mode_nth = mode_count

        print(f'Exploring "{mode}" now.')
        page.click(other_mode_head + str(other_mode_nth) + other_mode_tail)
        unique_ids_list = _tiktok_explore_page_unique_ids(page=page)

        for unique_id in unique_ids_list:
            unique_ids.add(unique_id)

        sleep(5)

    return list(unique_ids)

def rolling_page_down(page: Page) -> Page:
    """rolling tiktok page.

    args:
        page (Page): the page which is ready to rolling down.
    returns:
        page (Page): return the page which is rolled down.
    """
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    sleep(15)

    return page

def rolling_page_top(page: Page) -> Page:
    """rolling page to top.
    """
    page.evaluate("window.scrollTo(0, 0)")

    return page
