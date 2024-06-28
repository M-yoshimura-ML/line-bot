import re

from bots.weather_forecast import handle_location_message, handle_text_message
from utils.tools import reply


def bot(event):
    # hello bot
    # reply(event, 'hello')

    # identify keyword bot
    message_type = event['message']['type']
    if message_type == 'text':
        msg = event['message']['text']
        messages = check_message(msg)
        if len(messages) > 0:
            for message in messages:
                if message['pattern'] == 'greeting':
                    reply(event, message['text'])
                elif message['pattern'] == 'weather_forecast':
                    handle_text_message(event)
        else:
            reply(event, msg)

    elif message_type == 'location':
        handle_location_message(event)


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
