import os

import requests
from flask import Blueprint, request, jsonify, render_template

search_product_bp = Blueprint('search_product_bp', __name__)


@search_product_bp.route('/search', methods=['GET', 'POST'])
def search():
    keyword = ''
    results = []
    if request.method == 'POST':
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

        for item in items:
            item_info = item['Item']
            results.append({
                'name': item_info['itemName'],
                'price': item_info['itemPrice'],
                'shop': item_info['shopName'],
                'url': item_info['itemUrl']
            })

    return render_template('product/search_result.html', keyword=keyword, results=results)


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
