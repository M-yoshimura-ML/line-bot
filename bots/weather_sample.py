import requests
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('WEATHER_API_KEY')
base_url = os.environ.get('WEATHER_API_URL')

location = "Tokyo"
days = 3  # 予報日数
lang = 'ja'

# パラメータを設定
params = {
    "key": api_key,
    "q": location,
    "days": days,
    "lang": lang
}

response = requests.get(base_url, params=params)

# レスポンスをJSON形式で取得
data = response.json()

# データを表示
print(data)
