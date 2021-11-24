import logging
import os
from datetime import datetime
from google.cloud import storage


BUCKET_NAME = 'ps5hunter-screenshots'
SCREENSHOT_DIR = 'screenshots'


def upload_driver_screenshot(driver, name):
    """
    logic to save a driver screenshot and upload it to google cloud storage
    """
    fname = f'{name}-{datetime.now().isoformat()}.png'
    logging.info(f'saving screenshot {fname}')

    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    fpath = os.path.join(SCREENSHOT_DIR, fname)
    driver.save_screenshot(fpath)
    new_blob = bucket.blob(fname)
    new_blob.upload_from_filename(filename=fpath)