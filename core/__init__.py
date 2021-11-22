import logging
import google.cloud.logging
import os


# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
# TODO: better mechanism for swapping out logger.
if not os.getenv('DISABLE_CLOUD_LOGGER', False):
    client = google.cloud.logging.Client()
    client.setup_logging()

# logger = client.logger('default')
# logger.setLevel('INFO')

# logging.basicConfig(level=logging.INFO)