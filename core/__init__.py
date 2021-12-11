import logging
import google.cloud.logging
import os


# check if cloud logging is disabled ( so local sessions can run without cloud logging credentials )
if not os.getenv('DISABLE_CLOUD', False):
    client = google.cloud.logging.Client()
    client.setup_logging()  # by default this captures info and higher

logging.basicConfig(level=logging.INFO)
