import os
import re
from datetime import datetime

import pytz
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from pymongo import MongoClient

from utils.tools import reply

memo_bp = Blueprint('memo_bp', __name__)

load_dotenv()

credential = os.environ.get('MONGODB_URI')
client = MongoClient(credential)
db = client['linebot']
collection = db['memo']
user_collection = db['users']


def add_user(user_id):
    is_user_exit = check_user_exists(user_id)
    if not is_user_exit:
        result = user_collection.insert_one({
            "user_id": user_id
        })
        return jsonify({'msg': 'user is added', 'id': str(result.inserted_id)}), 201
    else:
        return jsonify({'msg': 'user already exits', 'user_id': user_id}), 400


def check_user_exists(user_id):
    user = user_collection.find_one({"user_id": user_id})
    return True if user else False


def add_memo_internal(memo):
    jp_tz = pytz.timezone('Asia/Tokyo')
    memo['created_at'] = datetime.now(jp_tz)
    if not memo['line_user_id']:
        return {'msg': 'line_user_id is required'}, 400
    if not check_user_exists(memo['line_user_id']):
        return {'msg': 'User not found'}, 404

    result = collection.insert_one(memo)
    return {'msg': 'memo is added', 'id': str(result.inserted_id)}, 201


def display_memo_internal(user_id):
    memos = list(collection.find(
        {"line_user_id": user_id}, {'_id': 0, 'memo': 1}).sort('created_at', -1))
    return memos, 200


def delete_memo_internal(user_id, memo):
    result = collection.delete_one({'line_user_id': user_id, 'memo': memo})
    if result.deleted_count:
        return {'msg': 'one memo is deleted'}, 200
    return {'msg': 'memo not found'}, 404


def delete_all_memos_internal(user_id):
    result = collection.delete_many({'line_user_id': user_id})
    if result.deleted_count:
        return {'msg': 'all memos deleted'}, 200
    return {'msg': 'memo not found'}, 404


@memo_bp.route('/add-memo', methods=['POST'])
def add_memo():
    memo = request.json
    response, status_code = add_memo_internal(memo)
    return jsonify(response), status_code


@memo_bp.route('/display-user-memo', methods=['GET'])
def display_memo():
    user_id = request.args.get('user_id', '')
    memos, status_code = display_memo_internal(user_id)
    return jsonify(memos), status_code


@memo_bp.route('/delete-memo', methods=['DELETE'])
def delete_memo():
    user_id = request.args.get('user_id', '')
    memo = request.args.get('memo', '')
    response, status_code = delete_memo_internal(user_id, memo)
    return jsonify(response), status_code


@memo_bp.route('/delete-all-memos', methods=['DELETE'])
def delete_all_memos():
    user_id = request.args.get('user_id', '')
    response, status_code = delete_all_memos_internal(user_id)
    return jsonify(response), status_code


def handle_memo(event, words):
    text = event['message']['text']
    user_id = event['source']['userId']
    response = {}
    """
    check words:
     [r"追加", r"買う", r"削除", r"買った", r"リスト表示", r"リストクリア",
      r"add", r"buy", r"remove", r"bought", r"show list", r"clear list"]
    """
    if words in [r"追加", r"買う", r"add", r"buy"]:
        keyword = re.sub(r"追加|買う|add|buy", "", text, flags=re.IGNORECASE).strip()
        memo = {'line_user_id': user_id, 'memo': keyword}
        response, _ = add_memo_internal(memo)
    elif words in [r"削除", r"買った", r"remove", r"bought"]:
        keyword = re.sub(r"削除|買った|remove|bought", "", text, flags=re.IGNORECASE).strip()
        response, _ = delete_memo_internal(user_id, keyword)
    elif words in [r"リスト表示", r"show list"]:
        memos, _ = display_memo_internal(user_id)
        memo_list = [memo['memo'] for memo in memos]
        response_text = "\n".join(memo_list)
        response = {'msg': response_text}
    elif words in [r"リストクリア", r"clear list"]:
        response, _ = delete_all_memos_internal(user_id)

    else:
        response['msg'] = 'メモを利用するには、以下のようにメッセージを送ってください。\n'
        response['msg'] += 'ex)XXXXXX 追加\n'
        response['msg'] += 'ex)XXXXXX 削除\n'
        response['msg'] += 'ex)XXXXXX リスト表示\n'
        response['msg'] += 'ex)XXXXXX リストクリア\n'
    reply(event, response['msg'])

