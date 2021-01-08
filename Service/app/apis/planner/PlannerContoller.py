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
            
            rs_arr = query_result[item['fld_user_planners']]

            # Loop to change ObjectId to string
            for index in range(len(rs_arr)):
                for key in rs_arr[index]:
                    # If there are ObjectId instances then change its value to string
                    if isinstance(rs_arr[index][key],ObjectId):
                        rs_arr[index][key] = str(rs_arr[index][key])
            return rs_arr
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def get_planner(self, pln_data = PlannerData()):
        try:
            query_result = clp_user.find_one({
                                '_id': ObjectId(pln_data.user_id)
                            },{
                                '_id' : 0,
                                item['fld_user_planners'] : 1
                            })
            
            rs_arr = query_result[item['fld_user_planners']]
            # Loop to change ObjectId to string
            for index in range(len(rs_arr)):
                if str(rs_arr[index]['_id']) != pln_data.planner_id:
                    continue
                for key in rs_arr[index]:
                    # If there are ObjectId instances then change its value to string
                    if isinstance(rs_arr[index][key],ObjectId):
                        rs_arr[index][key] = str(rs_arr[index][key])
                # set the result
                result = rs_arr[index]
                break
            return result
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def add_planner(self, pln_data = PlannerData()):
        try:
            logger.info("[{}] Prepair planner data to be save".format(pln_data.user_id))
            planner = pln_data.planner
            date = Date.get_datetime_now()
            tmp_arr = []
            new_planner = {
                   "_id" : ObjectId(),
                   item["fld_pln_name"] : planner['name'],
                   item["fld_pln_width"] : planner['width'],
                   item["fld_pln_height"] : planner['height'],
                   item["fld_pln_depth"] : planner['depth'],
                   item["fld_pln_unit_id"] : ObjectId(planner['unit']),
                   item["fld_pln_created_date"] : date,
                   item["fld_pln_latest_updated"] : date,
                   item["fld_pln_status"] : item["fld_pln_ACTIVE"],
                   item["fld_pln_boxes"] : tmp_arr,
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
        try:
            planner = pln_data.planner
            date = Date.get_datetime_now()
            fld_user_pln = "{}._id".format(item["fld_user_planners"])
            fld_pln_name = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_name'])
            fld_pln_width = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_width'])
            fld_pln_height = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_height'])
            fld_pln_depth = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_depth'])
            fld_pln_unit_id = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_unit_id'])
            fld_pln_latest_updated = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_latest_updated'])

            clp_user.update(
                {
                    '_id': ObjectId(pln_data.user_id),
                    fld_user_pln : ObjectId(pln_data.planner_id),
                },
                {
                    '$set' : 
                    { fld_pln_name: planner['name'] },
                    { fld_pln_width: planner['width'] },
                    { fld_pln_height: planner['height'] },
                    { fld_pln_depth: planner['depth'] },
                    { fld_pln_unit_id: ObjectId(planner['unit']) },
                    { fld_pln_latest_updated: date },
                },
            )

            logger.info("[{}] Edited a planner".format(pln_data.user_id))
            result = { 'mes' : "edited_planner", 'status' : "success"}

        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
        
    
    def delete_planner(self, pln_data = PlannerData()):
        try:
            date = Date.get_datetime_now()
            fld_user_pln = "{}._id".format(item["fld_user_planners"])
            fld_pln_status = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_status'])
            fld_pln_latest_updated = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_latest_updated'])
            
            clp_user.update(
                {
                    '_id': ObjectId(pln_data.user_id),
                    fld_user_pln : ObjectId(pln_data.planner_id),
                },
                {
                    '$set' : 
                    { fld_pln_status: item['fld_pln_REMOVE'] },
                    { fld_pln_latest_updated: date },
                },
            )

            logger.info("[{}] Deleted a planner".format(pln_data.user_id))
            result = { 'mes' : "deleted_planner", 'status' : "success"}

        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def is_duplicate_name(self, name):
        pass
    
    def render_container(self, pln_data = PlannerData()):
        pass

    def __del__(self):
        self.client.close()
   