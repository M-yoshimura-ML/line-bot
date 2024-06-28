import requests
import os

from dotenv import load_dotenv

from utils.tools import reply

load_dotenv()


def handle_message_event(event):
    message_type = event['message']['type']
    if message_type == 'text':
        handle_text_message(event)
    elif message_type == 'location':
        handle_location_message(event)


def handle_text_message(event):
    text = event['message']['text']
    if text.lower() == '位置情報を送信':
        reply_text = "現在位置情報を送信してください。"
        reply(event, reply_text)


def handle_location_message(event):
    latitude = event['message']['latitude']
    longitude = event['message']['longitude']
    weather_info = get_weather_by_location(latitude, longitude)
    reply_text = format_weather_info(weather_info)
    reply(event, reply_text)


def get_weather_by_location(lat, lon):
    lang = 'ja'
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
