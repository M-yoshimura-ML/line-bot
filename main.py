import atexit
import datetime
import json
import logging
import os

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask, request, render_template

from bots.memo import memo_bp
from bots.search_image import search_image_bp
from bots.search_product import search_product_bp
from bots.search_restaurant import search_restaurant_bp
from crons.notify import notify_time, notify_bp
from utils.hear import bot
from utils.tools import debug, push

app = Flask(__name__)
load_dotenv()
app.register_blueprint(notify_bp)
app.register_blueprint(search_product_bp)
app.register_blueprint(search_image_bp, url_prefix='/image')
app.register_blueprint(search_restaurant_bp, url_prefix='/restaurant')
app.register_blueprint(memo_bp)


@app.route('/test', methods=['GET'])
def test():
    data = {"message": "this is test route"}
    return data


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


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
    # logging.basicConfig()
    # logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=notify_time, trigger="interval", minutes=5)
    # scheduler.add_job(func=notify_time, trigger="interval", hours=1)
    # scheduler.add_job(func=notify_time, trigger="interval", days=1)
    # scheduler.start()
    # Shutdown the scheduler when exiting the app
    # atexit.register(lambda: scheduler.shutdown())

    app.run(debug=False)
