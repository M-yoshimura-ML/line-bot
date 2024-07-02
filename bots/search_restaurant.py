import os
import re

import requests
from flask import Blueprint, request, render_template

from utils.tools import reply

search_restaurant_bp = Blueprint('search_restaurant_bp', __name__)


@search_restaurant_bp.route('/search', methods=['GET', 'POST'])
def restaurant_search(page=1):
    keyword = ''
    address = ''
    results = []
    page_count = 0
    count = 30
    max_val = 1
    min_val = 0
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        keyword = request.form['keyword']
        address = request.form['address']
    else:
        keyword = request.args.get('keyword', '')
        address = request.args.get('address', '')

    if keyword:
        url = os.environ.get('HOT_PEPPER_API_URL')
        params = {
            'keyword': keyword,
            'key': os.environ.get('HOT_PEPPER_API_KEY'),
            'format': 'json',
            'start': page,
            'count': count,
            'address': address
        }
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる
            data = response.json()
            shops = data.get('results', [])
            page = shops['results_start']
            available_item_num = shops['results_available']
            page_count = int(available_item_num / 30)
            print('page_count:', page_count)
            max_val = max(1, page - 2)
            min_val = min(page + 2, page_count)
            for shop in shops['shop']:
                results.append({
                    'name': shop['name'],
                    'image': shop['logo_image'],
                    'address': shop['address'],
                    'open': shop['open'],
                    'close': shop['close'],
                    'url': shop['urls']['pc']
                })
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # HTTPエラーのログ
        except requests.exceptions.RequestException as req_err:
            print(f'Request error occurred: {req_err}')  # その他のリクエストエラーのログ
        except requests.exceptions.JSONDecodeError as json_err:
            print(f'JSON decode error occurred: {json_err}')  # JSONデコードエラーのログ
            print(f'Response text: {response.text}')  # レスポンス内容のログ
        except Exception as e:
            print('Something went wrong:', e)

    return render_template('restaurant/search_result.html',
                           keyword=keyword, results=results, page=page,
                           page_count=page_count, max_val=max_val, min_val=min_val,
                           address=address)

