import logging
from selenium.webdriver.common.by import By
from core.driver import new_driver
from core.notify import notify_in_stock, notify_of_error
from core.screenshot import upload_driver_screenshot

DEFAULT_RESPONSE = 'UNKNOWN'


def retry_or_notify(retries=2):
    """
    used to wrap a function and retry it n number of times, or notify_of_error once all retries are exhausted.
    """
    def decorator(f):
        def inner(*args, **kwargs):
            status = {
                'retries': retries,  # num allowed retries
                'errors': 0,
            }
            while status['retries'] >= 0:
                try:
                    return f(*args, **kwargs)  # a successful execution returns from the retry loop
                except Exception as e:
                    logging.error(f'caught error in {f.__name__}: {e} retries-remaining: {status["retries"]}')
                    status['retries'] -= 1
                    status['errors'] += 1

            num_err = status['errors']
            notify_of_error(f'{f.__name__} retried {retries} times, errored {num_err} times')
        return inner
    return decorator


@retry_or_notify(retries=2)
def amazon():
    """
    checks amazon site for ps5 inventory
    """
    logging.info('sniffing out amazon...')
    rsp = DEFAULT_RESPONSE
    with new_driver() as driver:
        url = 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/ref=as_li_ss_tl'
        driver.get(url)
        price_element = driver.find_element(By.CSS_SELECTOR, 'span.a-color-price')
        if price_element.text == 'Currently unavailable.':
            rsp = 'Sold Out'
        else:
            rsp = f'ps5 IN STOCK @ Amazon - {url}'
            notify_in_stock(rsp)
            upload_driver_screenshot(driver, 'amazon')
    print(f'Amazon: {rsp}')
    logging.info(f'Amazon: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def best_buy():
    """
    checks best buy site for ps5 inventory
    """
    logging.info('sniffing out best buy...')
    rsp = DEFAULT_RESPONSE
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
            upload_driver_screenshot(driver, 'best_buy')
    print(f'Best Buy: {rsp}')
    logging.info(f'Best Buy: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def costco():
    """
    checks costco site for ps5 inventory
    """
    logging.info('sniffing out costco...')
    rsp = DEFAULT_RESPONSE
    with new_driver() as driver:
        url = 'https://www.costco.com/sony-playstation-5-gaming-console-bundle.product.100813919.html'
        driver.get(url)
        img_overlay = driver.find_element(By.CSS_SELECTOR, 'img.oos-overlay')  # costco only indicator is image overlay
        if img_overlay.accessible_name == 'Out of Stock':
            rsp = 'Sold Out'
        else:
            rsp = f'ps5 IN STOCK @ Costco - {url}'
            notify_in_stock(rsp)
            upload_driver_screenshot(driver, 'costco')
    print(f'Costco: {rsp}')
    logging.info(f'Costco: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def gamestop():
    """
    checks gamestop site for ps5 inventory
    """
    logging.info('sniffing out gamestop...')
    rsp = DEFAULT_RESPONSE
    with new_driver() as driver:
        url = 'https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/playstation-5/229025.html'
        driver.get(url)
        elem = driver.find_element(By.ID, 'add-to-cart')
        if elem.text == 'UNAVAILABLE' or elem.text == 'NOT AVAILABLE':
            rsp = 'Sold Out'
        else:
            rsp = f'ps5 IN STOCK @ GameStop - {url}'
            notify_in_stock(rsp)
            upload_driver_screenshot(driver, 'gamestop')

    print(f'GameStop: {rsp}')
    logging.info(f'GameStop: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def target():
    """
    checks target site for ps5 inventory
    """
    logging.info('sniffing out target...')
    rsp = DEFAULT_RESPONSE
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
            upload_driver_screenshot(driver, 'target')
    print(f'Target: {rsp}')
    logging.info(f'Target: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def sony_ps5_disc():
    """
    checks sony site for ps5 disc edition inventory
    """
    logging.info('sniffing out sony ps5...')
    rsp = DEFAULT_RESPONSE
    with new_driver() as driver:
        url = 'https://direct.playstation.com/en-us/ps5'
        driver.get(url)
        ps5_disc_xpath = '/html/body/div[1]/div/div[3]/div/div[9]/hero-component/div/div/div[2]/hero-product-detail/div/div[3]/div[1]/p'
        disc_elem = driver.find_element(By.XPATH, ps5_disc_xpath)
        if disc_elem.text == 'Out of Stock':
            rsp = 'Sold Out'
        else:
            rsp = f'ps5 Disc IN STOCK @ sony - {url}'
            notify_in_stock(rsp)
            upload_driver_screenshot(driver, 'sony_ps5_disc')
    print(f'Sony: {rsp}')
    logging.info(f'Sony: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def sony_ps5_digital():
    """
    checks sony site for ps5 digital inventory
    """
    logging.info('sniffing out sony ps5-digital...')
    rsp = DEFAULT_RESPONSE
    with new_driver() as driver:
        url = 'https://direct.playstation.com/en-us/consoles/console/playstation5-digital-edition-console.3006647'
        driver.get(url)
        xpath = '/html/body/div[1]/div/div[3]/producthero-component/div/div/div[3]/producthero-info/div/div[5]/div[2]/p'
        elem = driver.find_element(By.XPATH, xpath)
        if elem.text == 'Out of Stock':
            rsp = 'Sold Out'
        else:
            rsp = f'ps5 Digital IN STOCK @ sony - {url}'
            notify_in_stock(rsp)
            upload_driver_screenshot(driver, 'sony_ps5_digital')
    print(f'Sony: {rsp}')
    logging.info(f'Sony: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def sony_ps4():
    """
    checks sony site for ps4 1TB inventory
    """
    logging.info('sniffing out sony ps4...')
    rsp = DEFAULT_RESPONSE
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
            upload_driver_screenshot(driver, 'sony_ps4')

    print(f'Sony: {rsp}')
    logging.info(f'Sony: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def adorama():
    """
    checks adorama site for ps5 inventory
    """
    logging.info('sniffing out adorama...')
    rsp = DEFAULT_RESPONSE
    with new_driver() as driver:
        url = 'https://www.adorama.com/so3005718.html'
        driver.get(url)
        buy_button = driver.find_element(By.CSS_SELECTOR, 'button.add-to-cart')
        if buy_button.text == 'Temporarily not available':
            rsp = 'Sold Out'
        else:
            rsp = f'ps5 IN STOCK @ Adorama - {url}'
            notify_in_stock(rsp)
            upload_driver_screenshot(driver, 'adorama')

    print(f'Adorama: {rsp}')
    logging.info(f'Adorama: {rsp}')
    return rsp


@retry_or_notify(retries=2)
def walmart():
    """
    note: walmart has bot detection... needs recaptcha handling.
    checks walmart site for ps5 inventory

    """
    # TODO: add recaptcha handling.
    # unfortunately walmart has bot detection. I may try to solve this at some point. for now walmart is not supported
    return DEFAULT_RESPONSE

    # logging.info('sniffing out walmart...')
    # rsp = default_response
    # with new_driver() as driver:
    #
    #     url = 'https://www.walmart.com/ip/PlayStation-5-Console/363472942?irgwc=1&sourceid=imp_wxw0K6wMnxyIT770gU38STG-UkG2yK3Rw2BP1o0&veh=aff&wmlspartner=imp_1943169&clickid=wxw0K6wMnxyIT770gU38STG-UkG2yK3Rw2BP1o0&sharedid=tomsguide-us&affiliates_ad_id=565706&campaign_id=9383'
    #     driver.get(url)
    #     # pprint(driver.page_source)
    #     if "Early access coming soon!" in driver.page_source:
    #         rsp = 'Sold Out'
    #     else:
    #         rsp = f'ps5 IN STOCK @ walmart - {url}'
    #         notify_in_stock(rsp)
    #         upload_driver_screenshot(driver, 'adorama')
    # print(f'Walmart: {rsp}')
    # logging.info(f'Walmart: {rsp}')
    # return rsp