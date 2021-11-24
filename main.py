import logging
import time
from flask import Flask
from concurrent.futures import ThreadPoolExecutor, as_completed
from core import hunt
from core.notify import notify, notify_of_error


app = Flask(__name__)

runloop_interval = 60  # for now, limit runloops to once every 60 seconds.


@app.route("/")
def index():
    """
    the only route - hunts all tracked sites for inventory
    :return: json dict of statuses
    """
    response = check_all()
    return response


def hunt_forever():
    """
    An infinite loop to check all sources once a minute. Used for local testing.
    The deployed bot lets the scheduler invoke this api, and loop is not used.
    """
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
    start = time.time()
    response = {}
    with ThreadPoolExecutor(max_workers=10) as e:
        futures = [
            e.submit(hunt.amazon),
            e.submit(hunt.best_buy),
            e.submit(hunt.costco),
            e.submit(hunt.gamestop),
            e.submit(hunt.target),
            e.submit(hunt.sony_ps4),
            e.submit(hunt.sony_ps5_disc),
            e.submit(hunt.sony_ps5_digital),
            e.submit(hunt.adorama),
        ]

        response['results'] = []
        for future in as_completed(futures):
            try:
                result = future.result()
                response['results'].append(result)
            except Exception as exc:
                notify_of_error(f'error getting result of future {exc}')

    end = time.time()
    duration = end - start
    logging.info(f'runloop took {duration} seconds')
    logging.info(f'inventory status: {response}')
    return response


if __name__ == '__main__':
    notify('ps5hunter started')
    hunt_forever()
    # app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
