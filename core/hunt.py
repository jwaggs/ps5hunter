import logging
from enum import Enum
from selenium.webdriver.common.by import By
from core.driver import new_driver
from core.notify import notify_in_stock, notify_of_error
from core.screenshot import upload_driver_screenshot


class HuntStatus(Enum):
    UNKNOWN = 'UNKNOWN'
    ERROR = 'ERROR'
    SOLD_OUT = 'SOLD_OUT'
    IN_STOCK = 'IN_STOCK'


def hunter(url: str, retries: int = 1):
    """
    wrapper for selenium web driver based hunts.
    injects a selenium web driver into the decorated function.
    if an error is raised inside the decorated function, this wrapper will retry the decorated function.
    if all retries are exhausted due to errors, this function will invoke notify_of_error.
    if the decorated function result is IN_STOCK, this function will invoke notify_in_stock.
    """
    if not url or url == '':
        raise ValueError('url is required for hunter decorator.')
    if retries < 0:
        raise ValueError('retry count cannot be negative. set to zero instead.')

    def decorator(f):
        def inner(*args, **kwargs):
            payload = {
                'name': f.__name__,  # capture name of decorated function.
                'url': url,  # set inside decorated function.
                'status': HuntStatus.UNKNOWN,  # set inside decorated function.
                'screenshot': None,  # if one is captured, this should be set with the url after upload.
                'attempts': 0,  # num times attempted.
                'errors': 0,  # num errors.
                'error': None,
            }

            allowed_attempts = 1 + retries  # we try 1 time plus the number of allowed retries.
            while payload['attempts'] <= allowed_attempts:
                payload['attempts'] += 1
                logging.info(f'hunt starting @ {payload}')
                with new_driver() as driver:
                    try:
                        # load page
                        driver.get(payload['url'])

                        # the decorated function can set response content on payload. this decorator will return it.
                        f(driver=driver, payload=payload, *args, **kwargs)

                        if payload['status'] is HuntStatus.IN_STOCK:
                            screenshot_url = upload_driver_screenshot(driver, payload['name'])
                            if screenshot_url:
                                payload['screenshot'] = screenshot_url
                            notify_in_stock(payload)

                        logging.info(f'hunt finished @ {payload}')
                        return payload
                    except Exception as e:
                        logging.error(f'caught error in {f.__name__}: {e} retries-remaining: {payload["retries"]}')
                        payload['status'] = HuntStatus.ERROR
                        payload['errors'] += 1
                        payload['error'] = e
                    finally:
                        if payload['status'] is HuntStatus.ERROR and payload['errors'] == allowed_attempts:
                            screenshot_url = upload_driver_screenshot(driver, payload['name'])
                            if screenshot_url:
                                payload['screenshot'] = screenshot_url
                            notify_of_error(payload)

            # return the state of this payload.
            return payload
        return inner
    return decorator


@hunter('https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/ref=as_li_ss_tl')
def amazon(driver, payload):
    """
    checks amazon site for ps5 inventory
    """
    # price_element = WebDriverWait(driver, 15).until(lambda d: d.find_element(By.CSS_SELECTOR, 'span.a-color-price'))
    price_element = driver.find_element(By.CSS_SELECTOR, 'span.a-color-price')
    if price_element.text == 'Currently unavailable.':
        payload['status'] = HuntStatus.SOLD_OUT
    else:
        payload['status'] = HuntStatus.IN_STOCK


@hunter('https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149')
def best_buy(driver, payload):
    """
    checks best buy site for ps5 inventory
    """
    buy_button = driver.find_element(By.CSS_SELECTOR, 'button.add-to-cart-button')
    if buy_button.text == 'Coming Soon' or buy_button.text == 'Sold Out':
        payload['status'] = HuntStatus.SOLD_OUT
    # elif buy_button.text == 'How Do I Buy This?':
    #     rsp = 'Limited AVAILABILITY!'
    #     notify_in_stock('Best Buy')
    else:
        payload['status'] = HuntStatus.IN_STOCK


@hunter('https://www.costco.com/sony-playstation-5-gaming-console-bundle.product.100813919.html')
def costco(driver, payload):
    """
    checks costco site for ps5 inventory
    """
    img_overlay = driver.find_element(By.CSS_SELECTOR, 'img.oos-overlay')  # costco only indicator is image overlay
    if img_overlay.accessible_name == 'Out of Stock':
        payload['status'] = HuntStatus.SOLD_OUT
    else:
        payload['status'] = HuntStatus.IN_STOCK


@hunter('https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/playstation-5/229025.html')
def gamestop(driver, payload):
    """
    checks gamestop site for ps5 inventory
    """
    elem = driver.find_element(By.ID, 'add-to-cart')
    if elem.text == 'UNAVAILABLE' or elem.text == 'NOT AVAILABLE':
        payload['status'] = HuntStatus.SOLD_OUT
    else:
        payload['status'] = HuntStatus.IN_STOCK


@hunter('https://direct.playstation.com/en-us/consoles/console/playstation5-console.3006646')
def sony_ps5_disc(driver, payload):
    """
    checks sony site for ps5 disc edition inventory
    """
    elem = driver.find_element_by_xpath("//link[@itemprop='availability']")
    href = elem.get_attribute('href')
    if href == 'https://schema.org/OutOfStock':
        payload['status'] = HuntStatus.SOLD_OUT
    else:
        payload['status'] = HuntStatus.IN_STOCK


@hunter('https://direct.playstation.com/en-us/consoles/console/playstation5-digital-edition-console.3006647')
def sony_ps5_digital(driver, payload):
    """
    checks sony site for ps5 digital inventory
    """
    xpath = '/html/body/div[1]/div/div[3]/producthero-component/div/div/div[3]/producthero-info/div/div[5]/div[2]/p'
    elem = driver.find_element(By.XPATH, xpath)
    if elem.text == 'Out of Stock':
        payload['status'] = HuntStatus.SOLD_OUT
    else:
        payload['status'] = HuntStatus.IN_STOCK


@hunter('https://direct.playstation.com/en-us/consoles/console/playstation4-1tb-console.3003348')
def sony_ps4(driver, payload):
    """
    checks sony site for ps4 1TB inventory
    """
    xpath = '/html/body/div[1]/div/div[3]/producthero-component/div/div/div[3]/producthero-info/div/div[5]/div[2]/p'
    elem = driver.find_element(By.XPATH, xpath)
    if elem.text == 'Out of Stock':
        payload['status'] = HuntStatus.SOLD_OUT
    else:
        payload['status'] = HuntStatus.IN_STOCK


@hunter('https://www.target.com/c/playstation-5-video-games/-/N-hj96d')
def target(driver, payload):
    """
    checks target site for ps5 inventory
    """
    xpath = '/html/body/div[1]/div/div[4]/div[4]/div/div/div[2]/p'
    driver.execute_script("window.scrollTo(0, 200)")  # scroll down for our screenshot. lots of banners
    banner = driver.find_element(By.XPATH, xpath)
    # driver.execute_script("arguments[0].scrollIntoView();", banner)
    if banner.text == 'Consoles will be viewable when inventory is available.':
        payload['status'] = HuntStatus.SOLD_OUT
    else:
        payload['status'] = HuntStatus.IN_STOCK
    return payload


@hunter('https://www.adorama.com/so3005718.html')
def adorama(driver, payload):
    """
    checks adorama site for ps5 inventory
    """
    buy_button = driver.find_element(By.CSS_SELECTOR, 'button.add-to-cart')
    if buy_button.text == 'Temporarily not available':
        payload['status'] = HuntStatus.SOLD_OUT
    else:
        payload['status'] = HuntStatus.IN_STOCK


# @hunter('https://www.walmart.com/ip/PlayStation-5-Console/363472942?irgwc=1&sourceid=imp_wxw0K6wMnxyIT770gU38STG-UkG2yK3Rw2BP1o0&veh=aff&wmlspartner=imp_1943169&clickid=wxw0K6wMnxyIT770gU38STG-UkG2yK3Rw2BP1o0&sharedid=tomsguide-us&affiliates_ad_id=565706&campaign_id=9383')
# def walmart(driver):
#     """
#     note: walmart has bot detection... needs recaptcha handling.
#     checks walmart site for ps5 inventory
#     """
#     # TODO: add recaptcha handling.
#     # unfortunately walmart has bot detection. I may try to solve this at some point. for now walmart is not supported
#     pass
