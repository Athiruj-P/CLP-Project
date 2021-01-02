# user_api
# Description : จัดการการเข้าสู่ระบบ/ออกจากระบบของผู้ใช้งาน และการกำหนด token
# Author : Athiruj Poositaporn
from flask import Flask, request, jsonify ,Blueprint
from pytz import timezone

from pymongo import MongoClient
from bson.json_util import dumps
import logging.config
from .. import db_config
from datetime import date , datetime

user_api = Blueprint('user_api', __name__)


login
Description : ปรับสถานะการเข้าสู่ระบบของผู้ใช้งาน
Author : Athiruj Poositaporn
@user_api.route("/login", methods=['POST'])
def login():
    try:
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if not username:
            result = {"mes": "Missing username parameter" , 'status' : 'error'}
            return result, 400
    except expression as identifier:
        pass
#     set_folder_name()
#     try:
#         username = request.form.get('username', None)
#         password = request.form.get('password', None)
#         logger.info("[{}] is logging in.".format(username))
#         if not username:
#             logger.warning("[{}] Missing username parameter.".format(username))
#             result = {"mes": "Missing username parameter" , 'status' : 'error'}
#             return result, 400
#         if not password:
#             logger.warning("[{}] Missing password parameter.".format(username))
#             result = {"mes": "Missing password parameter" , 'status' : 'error'}
#             return result, 400

#         query_result = DPML_db[collection].find_one({
#             db_config.item['fld_user_name']: username ,
#             db_config.item['fld_user_password']: password
#         })

#         if not query_result:
#             logger.warning("[{}] Wrong username or password.".format(username))
#             result = {"mes": "Wrong username or password." , 'status' : 'error'}
#             return result, 401
#         else:
#             DPML_db[collection].update(
#                 { db_config.item['fld_user_id']:query_result['user_id'] },
#                 { "$set":{ db_config.item['fld_user_login_status']:db_config.item['fld_user_status_login'] }}
#             )
        
#         query_result = DPML_db[role_collection].find_one({
#             db_config.item['fld_role_id']: int(query_result[db_config.item['fld_user_role_id']])
#         })

#         db_connect.close()
#         access_token = create_access_token(identity=username)
#         tokens = {
#             'access_token': create_access_token(identity=username),
#             'refresh_token': create_refresh_token(identity=username) 
#         }
#         logger.info("[{}] Response tokens to login.".format(username))
#         result = {'tokens':tokens, 'role':query_result['role_name'], 'status' : 'success'}
#         return result, 200
#     except Exception as identifier:
#         logger.error("{}.".format(str(identifier)))
#         result = {'mes' : str(identifier), 'status' : "system_error"}
#         return result , 400

# logout
# Description : ปรับสถานะการออกจากระบบของผู้ใช้งาน
# Author : Athiruj Poositaporn
# @user_api.route('/logout', methods=['POST'])
# def logout():
#     set_folder_name()
#     try:
#         username = request.form.get('username', None)
#         logger.info("[{}] Logging out.".format(username))
#         if not username:
#             logger.info("[{}] Missing username parameter.".format(username))
#             result = {"mes": "Missing username parameter." , 'status' : 'error'}
#             return result, 400

#         DPML_db[collection].update(
#             { db_config.item['fld_user_name']:username },
#             { "$set":{ db_config.item['fld_user_login_status']:db_config.item['fld_user_status_logout'] }}
#         )
#         logger.info("[{}] Response logout.".format(username))
#         result = {"mes": "Logout success" , 'status' : 'success'}
#         db_connect.close()
#         return result , 200
#     except Exception as identifier:
#         logger.error("{}.".format(str(identifier)))
#         result = {"mes": str(identifier) , 'status' : 'system_error'}
#         return result , 400
