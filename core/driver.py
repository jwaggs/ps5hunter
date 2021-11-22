from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote import remote_connection
import os
import logging
from contextlib import contextmanager


selenium_url = None
if os.environ.get('SELENIUM_URL') is not None:
    selenium_url = os.environ.get('SELENIUM_URL')  # required env
    logging.info(f'selenium url: {selenium_url}')
else:
    raise Exception('No remote Selenium webdriver provided in the environment.')


# def new_remote_driver():
#     global selenium_url
#     if os.environ.get('SELENIUM_OVERRIDE') is not None:
#         selenium_url = os.environ.get('SELENIUM_OVERRIDE')
#         logging.warning(f'WARNING: OVERWROTE SELENIUM URL to {selenium_url}')
#
#     selenium_connection = remote_connection.RemoteConnection(selenium_url, keep_alive=True)
#     chrome_driver = webdriver.Remote(selenium_connection, DesiredCapabilities.CHROME)
#     chrome_driver.set_page_load_timeout(120)
#     return chrome_driver


@contextmanager
def new_driver():
    global selenium_url
    if os.environ.get('SELENIUM_OVERRIDE') is not None:
        selenium_url = os.environ.get('SELENIUM_OVERRIDE')
        logging.warning(f'WARNING: OVERWROTE SELENIUM URL to {selenium_url}')

    selenium_connection = remote_connection.RemoteConnection(selenium_url, keep_alive=True)
    chrome_driver = webdriver.Remote(selenium_connection, DesiredCapabilities.CHROME)
    chrome_driver.set_page_load_timeout(120)
    error = None
    try:
        yield chrome_driver
    except Exception as e:
        error = e
    finally:
        chrome_driver.quit()  # quit the driver or future calls will hang
        if error:
            raise error
