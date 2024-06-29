import os
import re

import requests
from flask import Blueprint, request, render_template

from utils.tools import reply

search_product_bp = Blueprint('search_product_bp', __name__)


@search_product_bp.route('/search', methods=['GET', 'POST'])
def search(page=1):
    keyword = ''
    results = []
    page_count = 0
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        keyword = request.form['keyword']
    else:
        keyword = request.args.get('keyword', '')

    if keyword:
        url = os.environ.get('RAKUTEN_APP_API_URL')
        params = {
            'format': 'json',
            'keyword': keyword,
            'applicationId': os.environ.get('RAKUTEN_APP_ID'),
            'elements': "itemName,itemPrice,itemUrl,mediumImageUrls,count,first,hits,last,page,pageCount",
            'page': page
        }
        response = requests.get(url, params=params)
        data = response.json()

        items = data.get('Items', [])
        page = data.get('page')
        page_count = data.get('pageCount')

        for item in items:
            item_info = item['Item']
            results.append({
                'name': item_info['itemName'],
                'price': item_info['itemPrice'],
                'url': item_info['itemUrl'],
                'images': item_info['mediumImageUrls']
            })

    return render_template('product/search_result.html',
                           keyword=keyword, results=results, page=page, page_count=page_count)


def search_items(keyword=''):
    url = os.environ.get('RAKUTEN_APP_API_URL')
    params = {
        'format': 'json',
        'keyword': keyword,
        'applicationId': os.environ.get('RAKUTEN_APP_ID'),
        'elements': "itemName,itemPrice,itemUrl,mediumImageUrls,hits",
        'hits': 5
    }
    response = requests.get(url, params=params)
    data = response.json()

    items = data.get('Items', [])
    results = []
    for item in items:
        item_info = item['Item']
        results.append({
            'name': item_info['itemName'],
            'price': item_info['itemPrice'],
            'url': item_info['itemUrl'],
            'images': item_info['mediumImageUrls']
        })

    return results


def text_product_search(event):
    text = event['message']['text']
    # need Regex check
    keyword = re.sub(r"価格|price", "", text, flags=re.IGNORECASE).strip()

    if keyword:
        results = search_items(keyword)
        result_text = ""

        for item in results:
            result_text += f"商品名: {item['name']}\n"
            result_text += f"価格: {item['price']}円\n"
            result_text += f"URL: {item['url']}\n"
            result_text += "\n"  # line break per item

        reply(event, result_text)
    else:
        reply(event, '商品を検索するには、以下のようにメッセージを送ってください。\n ex)XXXXXX 価格')
