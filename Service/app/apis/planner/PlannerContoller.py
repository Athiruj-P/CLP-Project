# PlannerController
# Description : สำหรับ CRUD ข้อมูลของแผนการจัดเรียง
# Author : Athiruj Poositaporn

from flask import jsonify
import datetime, pytz
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid  import ObjectId
import logging
import logging.config
from ..db_config import item
from ..helper.PlannerData import PlannerData
from ..helper import Date

logger = logging.getLogger("planner_controller")

client = MongoClient(item["db_host"])
db = client.CLP_DB
clp_user =db.clp_user

class PlannerController:
    def get_all_planner(self, pln_data = PlannerData()):
        try:
            query_result = clp_user.find_one({
                                '_id': ObjectId(pln_data.user_id)
                            },{
                                '_id' : 0,
                                item['fld_user_planners'] : 1
                            })
            return query_result
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def get_planner(self, pln_data = PlannerData()):
        pass
    
    def add_planner(self, pln_data = PlannerData()):
        try:
            logger.info("[{}] Prepair planner data to be save".format(pln_data.user_id))
            planner = pln_data.planner
            date = Date.get_datetime_now()
            new_planner = {
                   item["fld_pln_name"] : planner['name'],
                   item["fld_pln_width"] : planner['width'],
                   item["fld_pln_height"] : planner['height'],
                   item["fld_pln_depth"] : planner['depth'],
                   item["fld_pln_unit_id"] : planner['unit'],
                   item["fld_pln_created_date"] : date,
                   item["fld_pln_latest_updated"] : date,
                   item["fld_pln_status"] : item["fld_pln_ACTIVE"],
                   item["fld_pln_boxes"] : None,
            }
            clp_user.update(
                {'_id': ObjectId(pln_data.user_id)},
                { '$push': {item["fld_user_planners"] : new_planner} }
            )
            logger.info("[{}] Added a planner to database".format(pln_data.user_id))
            result = { 'mes' : "added_planner", 'status' : "success"}
            return result
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def edit_planner(self, pln_data = PlannerData()):
        pass
    
    def delete_planner(self, pln_data = PlannerData()):
        pass
    
    def is_duplicate_name(self, name):
        pass
    
    def render_container(self, pln_data = PlannerData()):
        pass

    def __del__(self):
        self.client.close()
   