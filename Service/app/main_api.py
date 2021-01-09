from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import datetime, pytz
from bson.json_util import dumps
from apis.login.user_api import user_api
from apis.planner.planner_api import planner_api
from apis.box.box_api import box_api
from apis.db_config import item
from logging_config import dict_config, time_zone
import logging
import logging.config
from pytz import timezone

def timetz(*args):
    return datetime.datetime.now(tz).timetuple()

tz = timezone(time_zone)

logging.Formatter.converter = timetz
logging.config.dictConfig(dict_config)
logger = logging.getLogger("main")

app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(planner_api)
app.register_blueprint(box_api)
port = int(os.environ.get("PORT", 5000))
username = "Athiruj"

client = MongoClient(item["db_host"])
db = client.CLP_DB

@app.route("/")
def hello():
  logger.info("Test")
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