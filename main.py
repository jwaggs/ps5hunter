import datetime
import logging
import time
from flask import Flask
from flask import jsonify
from core.hunter import best_buy
from core.timer import RepeatedTimer
from core.notify import notify
import os
from threading import Thread
# Imports the Cloud Logging client library
import google.cloud.logging

# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.setup_logging()

app = Flask(__name__)

runloop_interval = 60  # for now, limit runloops to once every 60 seconds.


@app.route("/")
def index():
    """
    the only route - hunts all tracked sites for inventory
    :return: json dict of statuses
    """
    bb = best_buy()
    response = {
        'best buy': bb,
    }
    return response


# def delete_me_infinite_text_loop():
#     tick = 0
#     while True:
#         if tick % 5 == 0:
#             notify('delete_me_infinite_text_loop!!!')
#         print(f'tick {tick}')
#         time.sleep(2)
#         print(f'boom!')
#         time.sleep(1)
#         tick += 1


# this is no longer used because i deployed to GCP Cloud Run which does not handle long running jobs.
def hunt_forever():
    notify('hunting forever...')
    # run our scrapers on a repeated loop
    # RepeatedTimer(15, best_buy)
    tick = 0
    while tick >= 0:
        tick += 1
        if tick % 1000 == 0:
            # send summary every n runloop ticks.
            notify(f'inventory checker is on runloop tick: {tick}')

        start = time.time()
        check_all()
        end = time.time()
        duration = end - start
        logging.info(f'runloop {tick} took {duration} seconds')
        wait_time = runloop_interval - duration  # max of one loop per runloop_interval
        if 0 < wait_time < runloop_interval:
            logging.info(f'waiting {wait_time} seconds for next loop')
            time.sleep(wait_time)
        else:
            logging.info('skipping wait phase')


def check_all():
    best_buy()
    # TODO add other checks here.


if __name__ == '__main__':
    notify('ps5hunter started')
    hunt_forever()
    # app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
