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
from .BoxController import BoxController

box_api = Blueprint('box_api', __name__)
logger = logging.getLogger("box_api")

#get_box_std
#Description :
#Author : Athiruj Poositaporn
@box_api.route("/get_box_std", methods=['POST'])
def get_box_std():
    try:
        user_id = request.form.get('user_id', None)

        logger.info("[{}] Call API get_box_std()".format(user_id))
        # Check null value
        if not user_id:
            result = {"mes": "Missing user_id parameter" , 'status' : 'error'}
            return result, 400
        box_data = BoxData()
        box_data.user_id = user_id
        
        box_cont = BoxController()
        result = box_cont.get_box_std(box_data)
         
        return jsonify(result) , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400

#add_box
#Description :
#Author : Athiruj Poositaporn
@box_api.route("/add_box", methods=['POST'])
def add_box():
    try:
        user_id = request.form.get('user_id', None)
        pln_id = request.form.get('pln_id', None)

        new_data = {}
        new_data['name'] = request.form.get('name', None)
        new_data['width'] = request.form.get('width', None)
        new_data['height'] = request.form.get('height', None)
        new_data['depth'] = request.form.get('depth', None)
        new_data['unit'] = request.form.get('unit', None)
        new_data['qty'] = request.form.get('qty', None)
        new_data['color'] = request.form.get('color', None)

        logger.info("[{}] Call API get_planner()".format(user_id))
        # Check null value
        if not user_id:
            result = {"mes": "Missing user_id parameter" , 'status' : 'error'}
            return result, 400
        elif not pln_id:
            result = {"mes": "Missing pln_id parameter" , 'status' : 'error'}
            return result, 400
        
        for data in new_data:
            if not new_data[data]:
                result = {"mes": "Missing {} parameter".format(data) , 'status' : 'error'}
                return result, 400

        box_data = BoxData()
        box_data.user_id = user_id
        box_data.planner_id = pln_id
        box_data.boxes = new_data
        
        box_cont = BoxController()
        result = box_cont.add_box(box_data)
         
        return jsonify(result) , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400
