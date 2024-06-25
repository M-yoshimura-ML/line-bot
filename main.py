import os

from dotenv import load_dotenv
from flask import Flask, request

app = Flask(__name__)
load_dotenv()


@app.route('/test', methods=['GET'])
def test():
    data = {"message": "this is test route"}
    return data


@app.route('/', methods=['POST'])
def hear():
    input_data = request.data
    with open(os.environ.get('DEBUG_FILE'), 'wb') as f:
        f.write(input_data)
    return 'Data received', 200


if __name__ == '__main__':
    app.run(debug=True)
