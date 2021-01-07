# planner_api
# Description : จัดการการเข้าสู่ระบบ/ออกจากระบบของผู้ใช้งาน และการกำหนด token
# Author : Athiruj Poositaporn
from flask import Flask, request, jsonify ,Blueprint
import datetime, pytz
from pymongo import MongoClient
from bson.json_util import dumps
import logging
import logging.config
from ..db_config import item
from ..helper.PlannerData import PlannerData
from .PlannerContoller import PlannerController

planner_api = Blueprint('planner_api', __name__)
logger = logging.getLogger("planner_api")

#get_all_planner
#Description : 
#Author : Athiruj Poositaporn
@planner_api.route("/get_all_planner", methods=['POST'])
def get_all_planner():
    try:
        user_id = request.form.get('user_id', None)

        # Check null value
        if not user_id:
            result = {"mes": "Missing user_id parameter" , 'status' : 'error'}
            return result, 400
        pln_data = PlannerData()
        pln_data.user_id = user_id
        
        pln_cont = PlannerController()
        result = pln_cont.get_all_planner(pln_data)
         
        return jsonify(result)

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400
    finally:
        client.close()
