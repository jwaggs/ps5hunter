import logging
from selenium.webdriver.common.by import By
from core.driver import new_driver
from core.notify import notify_in_stock, notify_of_error, notify
from pprint import pprint


default_response = 'UNKNOWN'


def retry_or_notify(retries=2):
    """
    used to wrap a function and retry it n number of times, or notify_of_error once all retries are exhausted.
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
            rsp = f'ps5 IN STOCK @ Best Buy - {url}'
            notify_in_stock(rsp)
    print(f'Best Buy: {rsp}')
    logging.info(f'Best Buy: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def target():
    """
    checks target site for ps5 inventory
    """
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
            rsp = f'ps5 IN STOCK @ Target - {url}'
            notify_in_stock(rsp)
    print(f'Target: {rsp}')
    logging.info(f'Target: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def walmart():
    """
    checks walmart site for ps5 inventory
    note: walmart has bot detection... needs recaptcha handling.
    """
    logging.info('sniffing out walmart...')
    rsp = default_response
    with new_driver() as driver:
        url = 'https://www.walmart.com/ip/PlayStation-5-Console/363472942?irgwc=1&sourceid=imp_wxw0K6wMnxyIT770gU38STG-UkG2yK3Rw2BP1o0&veh=aff&wmlspartner=imp_1943169&clickid=wxw0K6wMnxyIT770gU38STG-UkG2yK3Rw2BP1o0&sharedid=tomsguide-us&affiliates_ad_id=565706&campaign_id=9383'
        driver.get(url)
        # # TODO: remove pprint
        # pprint(driver.page_source)
        if "Early access coming soon!" in driver.page_source:
            rsp = 'Sold Out'
        else:
            rsp = f'ps5 IN STOCK @ walmart - {url}'
            notify_in_stock(rsp)
    print(f'Walmart: {rsp}')
    logging.info(f'Walmart: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def sony_ps4():
    """
    checks sony site for ps5 inventory
    """
    logging.info('sniffing out sony...')
    rsp = default_response

    # PS4 loop
    with new_driver() as driver:
        url = 'https://direct.playstation.com/en-us/consoles/console/playstation4-1tb-console.3003348'
        driver.get(url)
        xpath = '/html/body/div[1]/div/div[3]/producthero-component/div/div/div[3]/producthero-info/div/div[5]/div[2]/p'
        elem = driver.find_element(By.XPATH, xpath)
        if elem.text == 'Out of Stock':
            rsp = 'Sold Out'
        else:
            rsp = f'ps4 1TB IN STOCK @ sony - {url}'
            notify_in_stock(rsp)

    print(f'Sony: {rsp}')
    logging.info(f'Sony: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def gamestop():
    """
    checks gamestop site for ps5 inventory
    """
    logging.info('sniffing out gamestop...')
    rsp = default_response
    with new_driver() as driver:
        url = 'https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/playstation-5/229025.html'
        driver.get(url)
        elem = driver.find_element(By.ID, 'add-to-cart')
        if elem.text == 'UNAVAILABLE':
            rsp = 'Sold Out'
        else:
            rsp = f'ps5 IN STOCK @ GameStop - {url}'
            notify_in_stock(rsp)

    print(f'GameStop: {rsp}')
    logging.info(f'GameStop: {rsp}')
    return rsp