import re

import requests
import os

from dotenv import load_dotenv

from utils.tools import reply

load_dotenv()

lang = 'ja'
jp_locations = [
    {'ja': '東京', 'en': 'Tokyo'},
    {'ja': '京都', 'en': 'Kyoto'},
    {'ja': '栃木', 'en': 'Tochigi'}
]


def handle_text_message(event):
    text = event['message']['text']
    is_matched = False
    for pattern in jp_locations:
        if re.search(pattern['ja'], text):
            handle_text_location_message(event, text)
            is_matched = True
            break

    if not is_matched:
        reply(event, '現在位置情報を送信してください。')


def get_weather_by_text(text):
    params = {
        'key': os.environ.get('WEATHER_API_KEY'),
        'q': text,
        'days': 3,
        "lang": lang
    }
    response = requests.get(os.environ.get('WEATHER_API_URL'), params=params)
    return response.json()


def get_weather_by_location(lat, lon):
    params = {
        'key': os.environ.get('WEATHER_API_KEY'),
        'q': f'{lat},{lon}',
        'days': 3,
        "lang": lang
    }
    response = requests.get(os.environ.get('WEATHER_API_URL'), params=params)
    return response.json()


def format_weather_info(data):
    location_name = data['location']['name']
    forecast = data['forecast']['forecastday'][0]
    date = forecast['date']
    condition = forecast['day']['condition']['text']
    temp_c = forecast['day']['avgtemp_c']

    return f"{location_name}の天気予報 ({date}):\n条件: {condition}\n平均気温: {temp_c}℃"


def handle_text_location_message(event, text):
    weather_info = get_weather_by_text(text)
    reply_text = format_weather_info(weather_info)
    reply(event, reply_text)


def handle_location_message(event):
    latitude = event['message']['latitude']
    longitude = event['message']['longitude']
    weather_info = get_weather_by_location(latitude, longitude)
    reply_text = format_weather_info(weather_info)
    reply(event, reply_text)