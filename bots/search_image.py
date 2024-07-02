import os
import random
import re

import requests
from flask import Blueprint, request, render_template

from utils.tools import reply, reply_image


search_image_bp = Blueprint('search_image_bp', __name__)


@search_image_bp.route('/search', methods=['GET', 'POST'])
def image_search(page=1):
    keyword = ''
    results = []
    page_count = 0
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        keyword = request.form['keyword']
    else:
        keyword = request.args.get('keyword', '')

    if keyword:
        url = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_URI')
        params = {
            'cx': os.environ.get('GOOGLE_CUSTOM_SEARCH_ENGINE_ID'),
            'key': os.environ.get('GOOGLE_CUSTOM_SEARCH_API_KEY'),
            'q': keyword,
            'searchType': 'image'
        }
        response = requests.get(url, params=params)
        data = response.json()

        items = data.get('items', [])
        # page = data.get('page')
        # page_count = data.get('pageCount')

        for item in items:
            results.append({
                'title': item['title'],
                'original': item['link'],
                'preview': item['image']['thumbnailLink']
            })

    return render_template('image/search_result.html',
                           keyword=keyword, results=results, page=page, page_count=page_count)


def search_image(keyword=''):
    url = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_URI')
    params = {
        'cx': os.environ.get('GOOGLE_CUSTOM_SEARCH_ENGINE_ID'),
        'key': os.environ.get('GOOGLE_CUSTOM_SEARCH_API_KEY'),
        'q': keyword,
        'searchType': 'image'
    }
    response = requests.get(url, params=params)
    data = response.json()

    items = data.get('items', [])
    if not items:
        return None

    item = random.choice(items)
    result = {
        'title': item['title'],
        'original': item['link'],
        'preview': item['image']['thumbnailLink']
    }

    return result


def keyword_image_search(event):
    text = event['message']['text']
    # need Regex check
    keyword = re.sub(r"画像|image", "", text, flags=re.IGNORECASE).strip()
    original = ''
    preview = ''

    if keyword:
        result = search_image(keyword)
        if result:
            original = result['original']
            preview = result['preview']

        reply_image(event, original, preview)
    else:
        reply(event, '画像を検索するには、以下のようにメッセージを送ってください。\n ex)XXXXXX 画像')
