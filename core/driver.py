from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote import remote_connection
import os
import logging
from contextlib import contextmanager


selenium_url = None
if os.environ.get('SELENIUM_URL') is not None:
    selenium_url = os.environ.get('SELENIUM_URL')  # required env
    logging.info(f'SELENIUM_URL: {selenium_url}')
else:
    raise Exception('No remote Selenium webdriver provided in the environment.')


@contextmanager
def new_driver():
    """
    driver generator.
    yields a driver, and ensures the chrome_driver.quit() method is called before re-raising the error
    """
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
