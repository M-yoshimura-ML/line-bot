import os

import requests
from flask import Blueprint, request, jsonify, render_template

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


@search_product_bp.route('/search-items', methods=['POST'])
def search_items():
    keyword = request.form['keyword']
    url = os.environ.get('RAKUTEN_APP_API_URL')
    params = {
        'format': 'json',
        'keyword': keyword,
        'applicationId': os.environ.get('RAKUTEN_APP_ID')
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
            'shop': item_info['shopName'],
            'url': item_info['itemUrl']
        })

    return jsonify(results)
