import json
import os

from dotenv import load_dotenv
from flask import Flask, request

from utils.hear import bot
from utils.tools import debug

app = Flask(__name__)
load_dotenv()


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
    app.run(debug=True)
