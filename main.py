import atexit
import datetime
import json
import logging
import os

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask, request

from utils.hear import bot
from utils.tools import debug, push

app = Flask(__name__)
load_dotenv()


def notify_time():
    jp_tz = pytz.timezone('Asia/Tokyo')
    time_info = '時報です。 ' + datetime.datetime.now(jp_tz).strftime('%Y-%m-%d %H:%M:%S')
    print(time_info)
    to = os.environ.get('USER_ID')
    push(to, time_info)


@app.route('/test', methods=['GET'])
def test():
    data = {"message": "this is test route"}
    return data


@app.route('/', methods=['POST'])
def main():
    input_data = request.data.decode('utf-8')
    debug('input', input_data)

    if input_data:
        events = json.loads(input_data).get('events', [])
        for event in events:
            bot(event)

    return 'Data received', 200


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=notify_time, trigger="interval", minutes=5)
    # scheduler.add_job(func=notify_time, trigger="interval", hours=1)
    # scheduler.add_job(func=notify_time, trigger="interval", days=1)
    scheduler.start()
    # Shutdown the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    app.run(debug=False)
