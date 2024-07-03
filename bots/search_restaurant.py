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


def search_restaurant(keyword='', address=''):
    results = []
    count = 10
    page = request.args.get('page', 1, type=int)

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
            print(f'HTTP error occurred: {http_err}')
        except requests.exceptions.RequestException as req_err:
            print(f'Request error occurred: {req_err}')
        except requests.exceptions.JSONDecodeError as json_err:
            print(f'JSON decode error occurred: {json_err}')
            print(f'Response text: {response.text}')
        except Exception as e:
            print('Something went wrong:', e)

    return results


def extract_keyword_address(text):
    # Define a regex pattern to capture keyword and address
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\t", "", text)
    text = re.sub(r"　", "", text)
    text = re.sub(r" ", "", text)
    pattern = re.compile(r"(.+?) 住所 (.+)")
    pattern2 = re.compile(r"(.+?) address (.+)")
    match = pattern.match(text)
    match2 = pattern2.match(text)
    if match:
        keyword = match.group(1).strip()
        address = match.group(2).strip()
        return keyword, address
    elif match2:
        keyword = match2.group(1).strip()
        address = match2.group(2).strip()
        return keyword, address
    else:
        return None, None


def text_restaurant_search(event):
    text = event['message']['text']
    # need Regex check
    keyword, address = extract_keyword_address(text)
    if keyword is None:
        keyword = re.sub(r"レストラン|restaurant", "", text, flags=re.IGNORECASE).strip()
    else:
        keyword = re.sub(r"レストラン|restaurant", "", keyword, flags=re.IGNORECASE).strip()

    if keyword:
        results = search_restaurant(keyword, address)
        result_text = ""

        for item in results:
            result_text += f"レストラン名: {item['name']}\n"
            result_text += f"住所: {item['address']}\n"
            result_text += f"オープン: {item['open']}\n"
            result_text += f"クローズ: {item['close']}\n"
            result_text += f"URL: {item['url']}\n"
            result_text += "\n"

        reply(event, result_text)
    else:
        reply(event, 'レストランを検索するには、以下のようにメッセージを送ってください。\n ex)XXXXXX レストラン \n 住所 YYYYY')
