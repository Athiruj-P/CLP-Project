# Box_api
# Description : 
# Author : Athiruj Poositaporn
from flask import Flask, request, jsonify ,Blueprint
import datetime, pytz
from pymongo import MongoClient
from bson.json_util import dumps
import logging
import logging.config
from ..db_config import item
from ..helper.BoxData import BoxData
from .BoxContoller import BoxController

box_api = Blueprint('box_api', __name__)
logger = logging.getLogger("box_api")

#get_std_box
#Description :
#Author : Athiruj Poositaporn
@planner_api.route("/get_std_box", methods=['POST'])
def get_std_box():
    try:
        user_id = request.form.get('user_id', None)

        logger.info("[{}] Call API get_std_box()".format(user_id))
        # Check null value
        if not user_id:
            result = {"mes": "Missing user_id parameter" , 'status' : 'error'}
            return result, 400
        pln_data = PlannerData()
        pln_data.user_id = user_id
        
        pln_cont = PlannerController()
        result = pln_cont.get_all_planner(pln_data)
         
        return jsonify(result) , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400
