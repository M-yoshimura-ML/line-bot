import json
import os
import datetime

import pytz
from flask import Blueprint

from utils.tools import push


notify_bp = Blueprint('notify', __name__)


def notify_time():
    jp_tz = pytz.timezone('Asia/Tokyo')
    time_info = '時報です。 ' + datetime.datetime.now(jp_tz).strftime('%Y-%m-%d %H:%M:%S')
    print(time_info)
    to = os.environ.get('USER_ID')
    push(to, time_info)


@notify_bp.route('/crons/notify', methods=['GET'])
def handler():
    notify_time()
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Cron job executed"})
    }
