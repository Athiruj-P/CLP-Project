from flask import Flask, request, jsonify
import os
from datetime import datetime
from pytz import timezone

from apis.login.user_api import user_api


app = Flask(__name__)
app.register_blueprint(user_api)
port = int(os.environ.get("PORT", 5000))
username = "Athiruj"

@app.route("/")
def hello():
    return "Hello" + username

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == "__main__":
     app.run(host='0.0.0.0', debug=True, port=port)