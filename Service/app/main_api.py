from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import datetime, pytz
from bson.json_util import dumps
from apis.login.user_api import user_api
from apis.planner.planner_api import planner_api
from apis.db_config import item

import logging
import logging.config

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.register_blueprint(user_api)
app.register_blueprint(planner_api)
port = int(os.environ.get("PORT", 5000))
username = "Athiruj"

client = MongoClient(item["db_host"])
db = client.CLP_DB

logger = logging.getLogger("main_api")

@app.route("/")
def hello():
  color = db.clp_color
  arr = []
  for item in color.find():
      logger.info(item['_id'])
      item['_id'] = str(item['_id'])
      arr.append(item)
  return jsonify(arr) , 200

@app.route("/all_user")
def test():
  user = db.clp_user
  arr = []
  for item in user.find():
      # item.pop('_id')
      logger.info(item['_id'])
      item['_id'] = str(item['_id'])
      arr.append(item)
  return jsonify(arr) , 200

@app.route("/test_time")
def test_time():
  tz = pytz.timezone('Asia/Bangkok')
  tmp = datetime.datetime.now(tz)
  logger.info("time => {}".format(tmp))
  return {'time':"{}".format(tmp)}

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == "__main__":
     app.run(host='0.0.0.0', debug=True, port=port)