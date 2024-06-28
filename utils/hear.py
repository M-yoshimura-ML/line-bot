import re

from bots.weather_forecast import handle_message_event
from utils.tools import reply


def bot(event):
    # hello bot
    # reply(event, 'hello')

    # echo bot
    # reply(event, event['message']['text'])

    # identify keyword bot
    messages = check_message(event['message']['text'])
    if len(messages) > 0:
        for message in messages:
            if message['pattern'] == 'greeting':
                reply(event, message['text'])
            elif message['pattern'] == 'weather_forecast':
                handle_message_event(event)


def check_message(message):
    messages = []
    # pattern list with Regex
    pattern_greetings = [r"hello", r"Good morning", r"おはよう", r"おはようございます"]

    # check message and if matches, return greeting message
    for pattern in pattern_greetings:
        if re.search(pattern, message):
            print("pattern matched")
            messages.append({'pattern': 'greeting', 'text': 'Good morning!'})

    pattern_weather_forecast = [r"天気", r"weather"]
    for pattern in pattern_weather_forecast:
        if re.search(pattern, message):
            messages.append({'pattern': 'weather_forecast', 'text': message})

    return messages
