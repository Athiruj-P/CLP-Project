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

class PlannerController:
    def __init__(self):
        try:
            self.client = MongoClient(item["db_host"])
            self.db = client.CLP_DB
            self.clp_user = self.db.clp_user
        except Exception as identifier:
            # logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def get_all_planner(self, pln_data):
        try:
            query_result = db.clp_user.find_one({
                                '_id': ObjectId(pln_data.user_id)
                            },{
                                '_id' : 0,
                                item['fld_user_planners'] : 1
                            })
            return query_result
        except Exception as identifier:
            # logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def get_planner(self, planner):
        pass
    
    def add_planner(self, planner):
        pass
    
    def edit_planner(self, planner):
        pass
    
    def delete_planner(self, planner):
        pass
    
    def is_duplicate_name(self, name):
        pass
    
    def render_container(self, planner):
        pass

    def __del__(self):
        self.client.close()
   