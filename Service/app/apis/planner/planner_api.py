# planner_api
# Description : 
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
#Description : ดึงข้อมูล planner ทั้งหมดจากผู้ใช้งาน
#Author : Athiruj Poositaporn
@planner_api.route("/get_all_planner", methods=['POST'])
def get_all_planner():
    try:
        user_id = request.form.get('user_id', None)

        logger.info("[{}] Call API get_all_planner()".format(user_id))
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

#get_planner
#Description : ดึงข้อมูล planner ตาม id จากผู้ใช้งาน
#Author : Athiruj Poositaporn
@planner_api.route("/get_planner", methods=['POST'])
def get_planner():
    try:
        user_id = request.form.get('user_id', None)
        pln_id = request.form.get('pln_id', None)

        logger.info("[{}] Call API get_planner()".format(user_id))
        # Check null value
        if not user_id:
            result = {"mes": "Missing user_id parameter" , 'status' : 'error'}
            return result, 400
        elif not pln_id:
            result = {"mes": "Missing pln_id parameter" , 'status' : 'error'}
            return result, 400
            
        pln_data = PlannerData()
        pln_data.user_id = user_id
        pln_data.planner_id = pln_id
        
        pln_cont = PlannerController()
        result = pln_cont.get_planner(pln_data)
        del pln_data
        return jsonify(result) , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400

#add_planner
#Description : เพิ่ม planner
#Author : Athiruj Poositaporn
@planner_api.route("/add_planner", methods=['POST'])
def add_planner():
    try:
        user_id = request.form.get('user_id', None)
        new_data = {}
        new_data['name'] = request.form.get('name', None)
        new_data['width'] = request.form.get('width', None)
        new_data['height'] = request.form.get('height', None)
        new_data['depth'] = request.form.get('depth', None)
        new_data['unit'] = request.form.get('unit', None)

        logger.info("[{}] Call API add_planner()".format(user_id))
        # Check null value
        for data in new_data:
            if not new_data[data]:
                result = {"mes": "Missing {} parameter".format(data) , 'status' : 'error'}
                return result, 400

        pln_data = PlannerData()
        pln_data.user_id = user_id
        pln_data.planner = new_data
        
        pln_cont = PlannerController()
        result = pln_cont.add_planner(pln_data)
        del pln_cont
        return result , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400

#edit_planner
#Description : แก้ไขข้อมูลของ planner
#Author : Athiruj Poositaporn
@planner_api.route("/edit_planner", methods=['POST'])
def edit_planner():
    try:
        user_id = request.form.get('user_id', None)
        pln_id = request.form.get('pln_id', None)

        new_data = {}
        new_data['name'] = request.form.get('name', None)
        new_data['width'] = request.form.get('width', None)
        new_data['height'] = request.form.get('height', None)
        new_data['depth'] = request.form.get('depth', None)
        new_data['unit'] = request.form.get('unit', None)

        logger.info("[{}] Call API edit_planner()".format(user_id))
        # Check null value
        if not pln_id:
            result = {"mes": "Missing {} parameter".format("pln_id") , 'status' : 'error'}
            return result, 400

        for data in new_data:
            logger.info("{} => {}".format(data,new_data[data]))
            if not new_data[data]:
                result = {"mes": "Missing {} parameter".format(data) , 'status' : 'error'}
                return result, 400

        pln_data = PlannerData()
        pln_data.user_id = user_id
        pln_data.planner_id = pln_id
        pln_data.planner = new_data
        
        pln_cont = PlannerController()
        result = pln_cont.edit_planner(pln_data)
        del pln_cont
        return result , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400

#delete_planner
#Description : ลบ planner ตาม ID ที่กำหนด (เปลี่ยนสถานะ)
#Author : Athiruj Poositaporn
@planner_api.route("/delete_planner", methods=['POST'])
def delete_planner():
    try:
        user_id = request.form.get('user_id', None)
        pln_id = request.form.get('pln_id', None)

        logger.info("[{}] Call API delete_planner()".format(user_id))
        # Check null value
        if not user_id:
            result = {"mes": "Missing {} parameter".format(user_id) , 'status' : 'error'}
            return result, 400
        elif not pln_id:
            result = {"mes": "Missing {} parameter".format(pln_id) , 'status' : 'error'}
            return result, 400

        pln_data = PlannerData()
        pln_data.user_id = user_id
        pln_data.planner_id = pln_id
        
        pln_cont = PlannerController()
        result = pln_cont.delete_planner(pln_data)
        del pln_cont
        return result , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400

#render_container
#Description : คำนวณการจัดเรียง Box ใน Container
#Author : Athiruj Poositaporn
@planner_api.route("/render_container", methods=['POST'])
def render_container():
    try:
        user_id = request.form.get('user_id', None)
        pln_id = request.form.get('pln_id', None)

        logger.info("[{}] Call API render_container()".format(user_id))
        # Check null value
        if not user_id:
            result = {"mes": "Missing {} parameter".format(user_id) , 'status' : 'error'}
            return result, 400
        elif not pln_id:
            result = {"mes": "Missing {} parameter".format(pln_id) , 'status' : 'error'}
            return result, 400

        pln_data = PlannerData()
        pln_data.user_id = user_id
        pln_data.planner_id = pln_id
        
        pln_cont = PlannerController()
        result = pln_cont.render_container(pln_data)
        del pln_cont
        return result , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400

#get_all_unit
#Description : ดึงข้อมูล unit ทั้งหมด
#Author : Athiruj Poositaporn
@planner_api.route("/get_all_unit", methods=['POST'])
def get_all_unit():
    try:
        user_id = request.form.get('user_id', None)

        logger.info("[{}] Call API get_all_unit()".format(user_id))
        # Check null value
        if not user_id:
            result = {"mes": "Missing user_id parameter" , 'status' : 'error'}
            return result, 400
            
        pln_data = PlannerData()
        pln_data.user_id = user_id
        
        pln_cont = PlannerController()
        result = pln_cont.get_all_unit()
        del pln_data
        return jsonify(result) , 200

    except Exception as identifier:
        logger.error("{}.".format(str(identifier)))
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400
