import re

from bots.search_product import text_product_search
from bots.weather_forecast import handle_location_message, handle_text_message
from utils.tools import reply, reply_image


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
                elif message['pattern'] == 'product_search':
                    text_product_search(event)
                elif message['pattern'] == 'image_search':
                    original = 'https://thumbnail.image.rakuten.co.jp/@0_mall/sevenheavenstore/cabinet/09673830/imgrc0089194103.jpg?_ex=128x128'
                    preview = 'https://thumbnail.image.rakuten.co.jp/@0_mall/sevenheavenstore/cabinet/09673830/imgrc0090744168.jpg?_ex=128x128'
                    reply_image(event, original, preview)
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

    pattern_product_search = [r"価格", r"price"]
    for pattern in pattern_product_search:
        if re.search(pattern, message):
            messages.append({'pattern': 'product_search', 'text': message})

    pattern_image_search = [r"画像", r"image"]
    for pattern in pattern_image_search:
        if re.search(pattern, message):
            messages.append({'pattern': 'image_search', 'text': message})

    return messages
