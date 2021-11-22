import logging
from selenium.webdriver.common.by import By
from core.driver import new_driver
from core.notify import notify_in_stock, notify_of_error, notify


default_response = 'UNKNOWN'


def retry_or_notify(retries=2):
    """
    used to wrap a function and retry it n number of times, or notify_of_error once all retries are exhausted
    """
    def decorator(f):
        def inner(*args, **kwargs):
            status = {
                'retries': retries,  # num allowed retries
                'errors': 0,  # if error count == num of allowed retries, we notify
            }
            while status['retries'] >= 0:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logging.error(f'caught error in retry decorator: {e} retries-remaining: {status["retries"]}')
                    status['retries'] -= 1
                    status['errors'] += 1
            num_err = status['errors']
            notify_of_error(f'retried {retries} times, errored {num_err} times')
            # return 'Status Unknown - All Retries Exhausted'
            # raise Exception("retried {} times".format(retries))
        return inner
    return decorator


@retry_or_notify(retries=2)
def best_buy():
    """
    checks best buy site for ps5 inventory
    """
    logging.info('sniffing out best buy...')
    rsp = 'Unknown Inventory Status'  # default response if anything goes wrong
    with new_driver() as driver:
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
            rsp = 'IN STOCK'
            notify_in_stock(f'best buy {url}')

    print(f'Best Buy: {rsp}')
    logging.info(f'Best Buy: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def target():
    logging.info('sniffing out target...')
    rsp = default_response
    with new_driver() as driver:
        url = 'https://www.target.com/c/playstation-5-video-games/-/N-hj96d'
        xpath = '/html/body/div[1]/div/div[4]/div[4]/div/div/div[2]/p'
        driver.get(url)
        banner = driver.find_element(By.XPATH, xpath)
        if banner.text == 'Consoles will be viewable when inventory is available.':
            rsp = 'Sold Out'
        else:
            rsp = 'IN STOCK'
            notify_in_stock(f'target {url}')
    print(f'Target: {rsp}')
    logging.info(f'Target: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def walmart():
    logging.info('sniffing out walmart...')
    rsp = default_response
    with new_driver() as driver:
        url = 'https://www.walmart.com/ip/Sony-PlayStation-5-Video-Game-Console/165545420'
        driver.get(url)
        print('PAGE SOURCE', driver.page_source)
        if "Early access coming soon!" in driver.page_source:
            print('FOUND MY STRING')
            rsp = 'Sold Out'
        else:
            rsp = 'IN STOCK'
            notify_in_stock(f'walmart {url}')
    print(f'Walmart: {rsp}')
    logging.info(f'Walmart: {rsp}')
    return rsp