import logging
import os
from datetime import datetime
from google.cloud import storage


BUCKET_NAME = 'ps5hunter-screenshots'
SCREENSHOT_DIR = 'screenshots'


def upload_driver_screenshot(driver, name, is_errored=False):
    """
    logic to save a driver screenshot and upload it to google cloud storage
    """
    try:
        # save screenshot
        prefix = 'error' if is_errored else 'alert'  # prefix based on whether this is an in-stock or error alert.
        fname = f'{prefix}-{name}-{datetime.now().isoformat()}.png'
        logging.info(f'saving screenshot {fname}')
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        fpath = os.path.join(SCREENSHOT_DIR, fname)
        driver.save_screenshot(fpath)
        logging.info(f'saved screenshot {fpath}')

        # upload screenshot
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        new_blob = bucket.blob(fname)
        new_blob.upload_from_filename(filename=fpath)
        logging.info(f'uploaded screenshot {fpath}')
        return fpath
    except Exception as e:
        logging.error(f'caught error handling screenshot: {e}')
