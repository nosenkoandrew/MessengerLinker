"""
This file serves as a local web-server  using Flask to receive incoming requests,
particularly for setting up the webhook or handling callbacks from Viber.
"""

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def callback():
    content_signature = request.headers.get('X-Viber-Content-Signature')

    if content_signature:
        return '', 200
    else:
        return 'Unauthorized', 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
