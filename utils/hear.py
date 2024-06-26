from utils.tools import reply


def bot(event):
    # hello bot
    # reply(event, 'hello')
    # echo bot
    reply(event, event['message']['text'])
