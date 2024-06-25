from flask import Flask, request

app = Flask(__name__)

DEBUG_FILE = './debug.txt'


@app.route('/', methods=['POST'])
def hear():
    input_data = request.data
    with open(DEBUG_FILE, 'wb') as f:
        f.write(input_data)
    return 'Data received', 200


if __name__ == '__main__':
    app.run(debug=True)
