from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote import remote_connection
import os
import logging

selenium_url = None
if os.environ.get('SELENIUM_URL') is not None:
    selenium_url = os.environ.get('SELENIUM_URL')  # required env
    logging.info(f'selenium url: {selenium_url}')
else:
    raise Exception('No remote Selenium webdriver provided in the environment.')


def new_remote_driver():
    global selenium_url
    if os.environ.get('SELENIUM_OVERRIDE') is not None:
        selenium_url = os.environ.get('SELENIUM_OVERRIDE')
        logging.warning(f'WARNING: OVERWROTE SELENIUM URL to {selenium_url}')

    selenium_connection = remote_connection.RemoteConnection(selenium_url, keep_alive=True)
    chrome_driver = webdriver.Remote(selenium_connection, DesiredCapabilities.CHROME)
    chrome_driver.set_page_load_timeout(120)
    return chrome_driver

# def new_driver():
#     options = webdriver.ChromeOptions()
#     options.add_argument('--disable-gpu')
#     # options.add_argument('--ignore-certificate-errors')
#     # options.add_argument('--allow-insecure-localhost')
#     options.add_argument("--headless")
#     options.add_argument("--window-size=1920, 1080")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
#     options.add_argument('--incognito')
#     # options.add_argument('--disable-dev-shm-usage')
#     # options.add_argument('--no-sandbox')
#
#     # path_to_driver = '/usr/local/bin/chromedriver'
#     path_to_driver = '/Users/jon/code/ps5/drivers/chromedriver'
#     driver = webdriver.Chrome(path_to_driver, options=options)
#     return driver

# def new_remote_driver():
#     options = webdriver.ChromeOptions()
#     options.add_argument('--disable-gpu')
#     # options.add_argument('--ignore-certificate-errors')
#     # options.add_argument('--allow-insecure-localhost')
#     options.add_argument("--headless")
#     options.add_argument("--window-size=1920, 1080")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
#     options.add_argument('--incognito')
#     # options.add_argument('--disable-dev-shm-usage')
#     # options.add_argument('--no-sandbox')
#
#     driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=options)
#     return driver