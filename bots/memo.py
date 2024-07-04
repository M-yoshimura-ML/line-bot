import os
from datetime import datetime

import pytz
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from pymongo import MongoClient


memo_bp = Blueprint('memo_bp', __name__)

load_dotenv()

credential = os.environ.get('MONGODB_URI')
client = MongoClient(credential)
db = client['linebot']
collection = db['memo']
user_collection = db['users']


def add_user(user_id):
    user = user_collection.find({"user_id": user_id})
    is_user_exit = check_user_exists(user_id)
    if not is_user_exit:
        result = user_collection.insert_one({
            "user_id": user_id
        })
        return jsonify({'msg': 'user is added', 'id': str(result.inserted_id)}), 201
    else:
        return jsonify({'msg': 'user already exits', 'user_id': user['user_id']}), 400


def check_user_exists(user_id):
    user = user_collection.find({"user_id": user_id})
    return True if user else False


@memo_bp.route('/add-memo', methods=['POST'])
def add_memo():
    memo = request.json
    jp_tz = pytz.timezone('Asia/Tokyo')
    memo['created_at'] = datetime.now(jp_tz)
    if not memo['line_user_id']:
        return jsonify({'msg': 'line_user_id is required'}), 400
    if not check_user_exists(memo['line_user_id']):
        return jsonify({'msg': 'User not found'}), 404

    result = collection.insert_one(memo)
    return jsonify({'msg': 'memo is added', 'id': str(result.inserted_id)}), 201


@memo_bp.route('/display-user-memo', methods=['GET'])
def display_memo():
    user_id = request.args.get('user_id')
    memos = list(collection.find(
        {"line_user_id": user_id}, {'_id': 0, 'memo': 1}).sort({'created_at': -1}))
    # for memo in memos:
    #     memo['_id'] = str(memo['_id'])
    return jsonify(memos), 200


