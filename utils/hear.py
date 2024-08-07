import re

from bots.memo import handle_memo
from bots.search_image import keyword_image_search
from bots.search_product import text_product_search
from bots.search_restaurant import text_restaurant_search
from bots.show_menu import reply_text_menu
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
                elif message['pattern'] == 'menu':
                    reply_text_menu(event)
                elif message['pattern'] == 'weather_forecast':
                    handle_text_message(event)
                elif message['pattern'] == 'product_search':
                    text_product_search(event)
                elif message['pattern'] == 'image_search':
                    keyword_image_search(event)
                elif message['pattern'] == 'restaurant_search':
                    text_restaurant_search(event)
                elif message['pattern'] == 'memo':
                    handle_memo(event, message['words'])
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

    pattern_menu = [r"メニュー", r"menu"]
    for pattern in pattern_menu:
        if re.search(pattern, message):
            messages.append({'pattern': 'menu', 'text': message})

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

    pattern_restaurant_search = [r"レストラン", r"restaurant"]
    for pattern in pattern_restaurant_search:
        if re.search(pattern, message):
            messages.append({'pattern': 'restaurant_search', 'text': message})

    pattern_memo = [r"追加", r"買う", r"削除", r"買った", r"リスト表示", r"リストクリア",
                    r"add", r"buy", r"remove", r"bought", r"show list", r"clear list"]
    for pattern in pattern_memo:
        if re.search(pattern, message):
            messages.append({'pattern': 'memo', 'text': message, 'words': pattern})

    return messages
