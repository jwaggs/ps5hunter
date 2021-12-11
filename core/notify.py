import logging
import os
from twilio.rest import Client


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
if not account_sid:
    raise Exception('TWILIO_ACCOUNT_SID env var required')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
if not auth_token:
    raise Exception('TWILIO_AUTH_TOKEN env var required')
number_from = os.getenv('TWILIO_FROM_NUM')
if not number_from:
    raise Exception('TWILIO_FROM_NUM env var required')
number_to = os.getenv('SMS_NOTIFY_NUM')
if not number_to:
    raise Exception('SMS_NOTIFY_NUM env var required')


def notify(message: str, media_url: str = None):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=number_to, from_=number_from, body=message, media_url=[media_url])
    logging.debug(f'sent message: {message} sid: {message.sid}')


def notify_in_stock(payload):
    logging.info(f'notifying IN STOCK: {payload}')
    notify(f'IN STOCK @ {payload["name"]}')
    notify(f'{payload["url"]}')
    screenshot = payload.get('screenshot', None)
    if screenshot:
        notify(f'{screenshot}')


def notify_of_error(payload):
    logging.error(f'notifying of error: {payload}')
    notify(f'ERROR @ {payload["name"]}')
    notify(f'{payload["url"]}')
    screenshot = payload.get('screenshot', None)
    if screenshot:
        notify(f'{screenshot}')
