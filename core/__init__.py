import logging
import google.cloud.logging
import os


# TODO: better mechanism for swapping out logger.
if not os.getenv('DISABLE_CLOUD_LOGGER', False):
    # check if cloud logging is disabled ( so local sessions can run without cloud logging credentials )
    client = google.cloud.logging.Client()
    client.setup_logging()  # by default this captures info and higher

# logger = client.logger('default')
# logger.setLevel('INFO')
