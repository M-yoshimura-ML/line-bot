import re

from utils.tools import reply


def bot(event):
    # hello bot
    # reply(event, 'hello')

    # echo bot
    # reply(event, event['message']['text'])

    # identify keyword bot
    message = check_message(event['message']['text'])
    if message:
        reply(event, message)


def check_message(message):
    # pattern list with Regex
    patterns = [r"hello", r"Good morning", r"おはよう", r"おはようございます"]

    # check message and if matches, return greeting message
    for pattern in patterns:
        if re.search(pattern, message):
            print("pattern matched")
            return 'good morning!'

    return None
