import datetime
import logging
import time
from flask import Flask
from flask import jsonify
from core.hunter import best_buy, target, walmart
from core.timer import RepeatedTimer
from core.notify import notify


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
    response = {}  # json dict of store statuses
    # response['Walmart'] = walmart()  # damnit - walmart has recaptcha blocking me
    response['Best Buy'] = best_buy()
    response['Target'] = target()
    logging.info(f'checked all stores: {response}')

    # TODO: remove pprint & notify here. only log each loop.
    # from pprint import pprint
    # pprint(response)
    # notify(f'statuses:\n\n{response}')
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


if __name__ == '__main__':
    notify('ps5hunter started')
    hunt_forever()
    # app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
