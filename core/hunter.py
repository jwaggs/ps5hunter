import logging

from selenium.webdriver.common.by import By

from core.driver import new_remote_driver
from core.notify import notify_in_stock, notify_of_error, notify
from core.timer import timeout

count_err = 0  # used to track sequential errors to suppress notifications


# @timeout(60)  # timeout not allowed on background thread since it uses signal
def best_buy():
    """
    checks best buy site for ps5 inventory
    """
    logging.info('sniffing out best buy...')
    global count_err
    rsp = 'Unknown Inventory Status'  # default response if anything goes wrong
    driver = new_remote_driver()
    try:
        url = 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'
        driver.get(url)
        buy_button = driver.find_element(By.CSS_SELECTOR, 'button.add-to-cart-button')
        if buy_button.text == 'Coming Soon':
            rsp = 'Coming Soon'
        elif buy_button.text == 'Sold Out':
            rsp = 'Sold Out'
        # elif buy_button.text == 'How Do I Buy This?':
        #     rsp = 'Limited AVAILABILITY!'
        #     notify_in_stock('Best Buy')
        else:
            rsp = 'In Stock'
            notify_in_stock(f'best buy {url}')
        count_err = 0
    except Exception as e:
        count_err += 1
        err_message = f'caught error {e}'
        logging.error(err_message)
        if count_err > 1:
            notify_of_error(err_message)
    finally:
        driver.quit()
    logging.info(f'Best Buy: {rsp}')
    return rsp


def target():
    pass