import json
import requests
import os

from dotenv import load_dotenv

load_dotenv()
DEBUG_FILE = os.environ.get('DEBUG_FILE', '/tmp/debug.txt')


def debug(key, value):
    print(f"{key}: {value}")
    print(f"DEBUG_FILE path: {DEBUG_FILE}")

    try:
        # make sure the directory and create if necessary
        os.makedirs(os.path.dirname(DEBUG_FILE), exist_ok=True)

        with open(DEBUG_FILE, 'a') as f:
            message = f"{key}: {value}\n"
            f.write(message)
            f.flush()
    except Exception as e:
        print(f"Error writing to debug file: {e}")


def post(url, obj):
    json_data = json.dumps(obj)
    debug('output', json_data)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("LINE_MESSAGING_API_TOKEN")}'
    }
    response = requests.post(f'https://api.line.me/v2/bot/message/{url}',
                             headers=headers, data=json_data)
    debug('result', response.text)


def reply(event, text):
    obj = {
        'replyToken': event['replyToken'],
        'messages': [{'type': 'text', 'text': text}]
    }
    post('reply', obj)


def push(to, text):
    obj = {
        'to': to,
        'messages': [{'type': 'text', 'text': text}]
    }

    post('push', obj)
