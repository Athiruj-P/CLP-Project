from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import db_config


app = Flask(__name__)

username = "Athiruj"

@app.route("/")
def hello():
    return "Hello" + username

# Get all user
@app.route('/get_all_user', methods=['get'])
def get_all_user():
    users = []
    for i in DPML_db[user_collection].find():
        i.pop('_id')
        users.append(i)
    db_connect.close()
    result = jsonify(users)
    return result

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response
