# user_api
# Description : จัดการการเข้าสู่ระบบ/ออกจากระบบของผู้ใช้งาน
# Author : Athiruj Poositaporn
from flask import Flask, request, jsonify ,Blueprint
import datetime, pytz
from pymongo import MongoClient
from bson.json_util import dumps
import logging
import logging.config
from ..db_config import item

user_api = Blueprint('user_api', __name__)
logger = logging.getLogger("user_api")

client = MongoClient(item["db_host"])
db = client.CLP_DB

#login
#Description : ปรับสถานะการเข้าสู่ระบบของผู้ใช้งาน
#Author : Athiruj Poositaporn
@user_api.route("/login", methods=['POST'])
def login():
    try:
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        # logger.info("{} {}".format(username,password))
        # Check null value
        if not username:
            result = {"mes": "Missing username parameter" , 'status' : 'error'}
            return result, 200
        # Check null value
        elif not password:
            result = {"mes": "Missing password parameter" , 'status' : 'error'}
            return result, 200
            
        # Query user from DB
        query_result = db[item['db_col_user']].find_one({
           item['fld_user_name']: username ,
           item['fld_user_password']: password
        })

        # Query not found
        if not query_result:
            logger.warning("[{}] Wrong username or password".format(username))
            result = {"mes": "Wrong username or password" , 'status' : 'error'}
            return result, 200
        # Set user login status
        else:
            db[item['db_col_user']].update(
                { '_id': query_result['_id'] },
                { "$set": 
                    {   item['fld_user_status']: item['fld_user_LOGIN'],
                        item['fld_user_latest_login']: get_datetime_now()
                    }
                }
            )
        
        result = {'status' : 'success', 'user_id': str(query_result['_id'])}
        return result, 200 

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 200
    finally:
        client.close()

# logout
# Description : ปรับสถานะการออกจากระบบของผู้ใช้งาน
# Author : Athiruj Poositaporn
@user_api.route('/logout', methods=['POST'])
def logout():
    try:
        username = request.form.get('username', None)
        # Check null value
        if not username:
            result = {"mes": "Missing username parameter" , 'status' : 'error'}
            return result, 400

        # Set user logout status
        db[item['db_col_user']].update(
            { item['fld_user_name']:username },
            { "$set":{ item['fld_user_status']:item['fld_user_LOGOUT'] }}
        )
        result = {'status' : 'success'}
        return result , 200
    except Exception as identifier:
        result = {"mes": str(identifier) , 'status' : 'system_error'}
        return result , 200
    finally:
        client.close()

def get_datetime_now():
    tz = pytz.timezone('Asia/Bangkok')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S.%f')
