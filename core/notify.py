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


def notify(message: str):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=number_to, from_=number_from, body=message)
    logging.info(f'sent message: {message} sid: {message.sid}')


def notify_in_stock(name: str):
    notify(f'ps5 IN STOCK @ {name}!')


def notify_of_error(error: str):
    logging.error(f'notifying of error: {error}')
    notify(f'error checking ps5 stock: {error}')
