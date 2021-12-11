from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote import remote_connection
import os
import logging
from contextlib import contextmanager

# this flag will use a local chromedriver instead of
disable_cloud = os.environ.get('DISABLE_CLOUD', False)


selenium_url = None
if os.environ.get('SELENIUM_URL') is not None:
    selenium_url = os.environ.get('SELENIUM_URL')  # required env
    logging.info(f'SELENIUM_URL: {selenium_url}')
else:
    raise Exception('No remote Selenium webdriver provided in the environment.')


@contextmanager
def new_driver():
    """
    selenium driver generator.
    yields a driver, and ensures the chrome_driver.quit() method is called before re-raising the error
    """
    if disable_cloud:
        logging.warning(f'disabling cloud driver. using local driver instead.')
        with new_local_driver() as dr:
            yield dr
        return

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


@contextmanager
def new_local_driver():
    """
    selenium driver generator for when chromedriver is on the local dev machine.
    yields a driver, and ensures the chrome_driver.quit() method is called before re-raising the error
    """
    chrome_driver = webdriver.Chrome(executable_path=selenium_url)
    chrome_driver.set_page_load_timeout(120)
    # chrome_driver.set_window_position(0, 0)
    chrome_driver.set_window_size(1200, 1700)
    error = None
    try:
        yield chrome_driver
    except Exception as e:
        print('EXCEPTION CAUGHT IN DRIVER MANAGER', e)
        error = e
    finally:
        chrome_driver.quit()  # quit the driver or future calls will hang
        if error:
            raise error
