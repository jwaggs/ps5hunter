import logging
import os
from twilio.rest import Client


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
assert account_sid is not None
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
assert auth_token is not None
number_from = os.getenv('TWILIO_PHONE_NUM')
assert number_from is not None
number_to = os.getenv('SMS_NOTIFY_NUM')
assert number_to is not None


def notify(message: str):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=number_to, from_=number_from, body=message)
    logging.info(f'sent message: {message} sid: {message.sid}')


def notify_in_stock(name: str):
    notify(f'ps5 IN STOCK @ {name}!')


def notify_of_error(error: str):
    logging.error(f'notifying of error: {error}')
    notify(f'error checking ps5 stock: {error}')
