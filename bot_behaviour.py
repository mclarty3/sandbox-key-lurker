import sys
import time
import threading
import traceback

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from typing import Tuple

asset_party_url = 'https://asset.party/get/developer/preview'

element_xpath_dict = {
    'sbox_steam_login_button': '/html/body/header/div[1]/div/div/div/a[3]',
    'steam_login_field': '//*[@id="steamAccountName"]',
    'steam_pwd_field': '//*[@id="steamPassword"]',
    'steam_login_button': '//*[@id="imageLogin"]',
    'sbox_gamecards': '/html/body/div[4]/div/div/div/div/gamecards',
    'sbox_enter_queue_button': '//button[@class="button is-large is-primary"]'
}

get_element = lambda driver, element: driver.find_element('xpath', element_xpath_dict[element])
bot_print = lambda id, msg: print(f'[{id}] {msg}')


def start_bot(event: threading.Event, id: int, steam_creds: Tuple[str, str], headless: bool = False,
              silent: bool = False, super_silent: bool = False, run_once: bool = False) -> None:
    """Start a new bot with its own webdriver instance.

    Parameters
    ----------
    event : threading.Event
        Event linked to the thread running this method. Used to signal when the bot has finished.

    id : int
        The unique id of the bot.

    steam_creds : Tuple[str, str]
        The username and password of the bot.

    headless : bool
        Whether or not to run the bot in headless mode (no browser GUI).

    silent : bool
        Will only output to console when the bot is initialized, when the queue restarts, and when the bot is killed

    super_silent : bool
        Will not output to console at all.

    run_once : bool
        If true, the bot will exit after the "Enter" button is re-enabled, rather than waiting until the queue is
        enabled again.

    """
    if not super_silent:
        bot_print(id, f"Initializing Chrome driver{' (headless)' if headless else ''}")
    try:
        driver = __init_chrome_driver(headless)
        __run_bot(event, driver, id, steam_creds, silent, super_silent, run_once)
    except Exception:
        bot_print(id, 'Error:')
        print(traceback.format_exc())
        driver.close()
        sys.exit(1)


def __init_chrome_driver(headless: bool = False) -> webdriver.Chrome:
    """Starts a new Chrome webdriver instance."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')                                    # Don't open the webdriver browser
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Prevent terminal logging
    driver = webdriver.Chrome(options=options)
    return driver


def __init_asset_party(driver: webdriver.Chrome) -> None:
    """Navigates to the Asset Party page and clicks the button to login to Steam."""
    driver.get(asset_party_url)

    WebDriverWait(driver, timeout=10).until(lambda d: 'Log In' in get_element(d, 'sbox_steam_login_button').text)

    # Funky work-around that seems to work
    try:
        get_element(driver, 'sbox_steam_login_button').click()
    except Exception:
        get_element(driver, 'sbox_steam_login_button').click()


def __login_to_steam(driver: webdriver.Chrome, user: str, pwd: str) -> None:
    """Enters the given credentials into the Steam login page and attempts to login."""
    WebDriverWait(driver, timeout=5).until(lambda d: get_element(d, 'steam_login_field'))

    get_element(driver, 'steam_login_field').send_keys(user)
    get_element(driver, 'steam_pwd_field').send_keys(pwd)
    get_element(driver, 'steam_login_button').click()


def __run_bot(event: threading.Event, driver: webdriver.Chrome, id: int, steam_creds: Tuple[str, str],
            silent: bool = False, super_silent: bool = False, run_once: bool = False) -> None:
    """The main loop of the bot. Waits for the queue to be enabled, then enters the queue and waits for the button to
    be re-enabled, looping infinitely unless run_once is set to True."""
    user, pwd = steam_creds

    if not silent:
        bot_print(id, 'Navigating to Asset Party site')
    __init_asset_party(driver)

    if not silent:
        bot_print(id, 'Logging in to Steam')
    __login_to_steam(driver, user, pwd)

    WebDriverWait(driver, timeout=5).until(lambda d: get_element(d, 'sbox_gamecards'))

    if not silent:
        bot_print(id, 'Returning to Asset Party site')
    driver.get(asset_party_url)

    WebDriverWait(driver, timeout=5).until(lambda d: get_element(d, 'sbox_enter_queue_button'))

    while not event.is_set():
        while get_element(driver, 'sbox_enter_queue_button').get_attribute('disabled') == 'true':
            if not silent:
                bot_print(id, 'Waiting for developer preview queue to become available...')
            time.sleep(5)

        if not silent:
            bot_print(id, 'Entering developer preview')
        get_element(driver, 'sbox_enter_queue_button').click()

        while get_element(driver, 'sbox_enter_queue_button').get_attribute('disabled') != 'true':
            if not silent:
                bot_print(id, 'Waiting for keys to be distributed...')
            time.sleep(5)

        if not super_silent:
            bot_print(id, 'Developer preview restarted, hopefully I got a key!')

        if run_once:
            if not super_silent:
                bot_print(id, 'Quitting.')
            break

    driver.close()
