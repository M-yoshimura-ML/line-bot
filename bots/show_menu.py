from utils.tools import reply


def reply_text_menu(event):
    text_message = "このLINE channelでは次のことができます。\n\n"
    text_message += "1.天気予報 \n"
    text_message += "ex)東京 天気 \n"
    text_message += "または位置情報を送信してください。 \n\n"
    text_message += "2.商品検索 \n"
    text_message += "ex)ELDEN RING 価格 \n\n"
    text_message += "3.画像検索 \n"
    text_message += "ex)ELDEN RING 画像 \n\n"
    text_message += "4.レストラン検索 \n"
    text_message += "ex)焼肉 レストラン \n"
    text_message += "ex)焼肉 レストラン 住所 東京 \n"

    reply(event, text_message)
