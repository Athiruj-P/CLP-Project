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
from ..err_msg import msg
import re

logger = logging.getLogger("planner_controller")

client = MongoClient(item["db_host"])
db = client.CLP_DB
clp_user = db[item['db_col_user']]
clp_unit = db[item['db_col_unit']]

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
            arr = []
            # Loop to change ObjectId to string
            for index in range(len(rs_arr)):
                # Continue if planner's status is REMOVE (0)
                if rs_arr[index][item['fld_pln_status']] != item['fld_pln_ACTIVE']:
                    continue
                rs_arr[index].pop(item['fld_pln_boxes'])
                for key in rs_arr[index]:
                    # If there are ObjectId instances then change its value to string
                    if isinstance(rs_arr[index][key],ObjectId):
                        rs_arr[index][key] = str(rs_arr[index][key])
                # Store ACTIVE planner
                arr.append(rs_arr[index])
            return arr
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def get_planner(self, pln_data = PlannerData()):
        try:
            srt_fild = "{}._id.$".format(item['fld_user_planners'])
            query_result = clp_user.find_one(
                {
                    item['fld_user_planners']:{
                        '$elemMatch': {"_id" : ObjectId(pln_data.planner_id) }
                    }
                },
                {
                    srt_fild : 1
                }
            )
            
            if not query_result:
                return None
            else:
                query_result = query_result[item['fld_user_planners']][0]
                for key in query_result:
                    if key == item['fld_pln_boxes']:
                        for index in query_result[key]:
                            query_result[key][index] =str(query_result[key][index])
                    if isinstance(query_result[key],ObjectId):
                        query_result[key] = str(query_result[key])
                return query_result
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def add_planner(self, pln_data = PlannerData()):
        try:
            logger.info("[{}] Prepair planner data to be save".format(pln_data.user_id))
            planner = pln_data.planner

            # Validation
            if not self.check_name_format(planner['name']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_name_format']))
                raise TypeError(msg['wrong_name_format'])
            elif not self.is_number(planner['width']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_width']))
                raise TypeError(msg['wrong_width'])
            elif not self.is_number(planner['height']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_height']))
                raise TypeError(msg['wrong_height'])
            elif not self.is_number(planner['depth']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_depth']))
                raise TypeError(msg['wrong_depth'])
            elif not self.check_unit_id(planner['unit']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_unit_id']))
                raise TypeError(msg['wrong_unit_id'])

            date = Date.get_datetime_now()
            tmp_arr = []
            new_planner = {
                   "_id" : ObjectId(),
                   item["fld_pln_name"] : planner['name'],
                   item["fld_pln_width"] :float( planner['width']),
                   item["fld_pln_height"] :float( planner['height']),
                   item["fld_pln_depth"] :float( planner['depth']),
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
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def edit_planner(self, pln_data = PlannerData()):
        try:
            logger.info("[{}] Prepair planner data to be save".format(pln_data.user_id))
            planner = pln_data.planner

            # Validation
            if not self.check_name_format(planner['name']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_name_format']))
                raise TypeError(msg['wrong_name_format'])
            elif not self.is_number(planner['width']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_width']))
                raise TypeError(msg['wrong_width'])
            elif not self.is_number(planner['height']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_height']))
                raise TypeError(msg['wrong_height'])
            elif not self.is_number(planner['depth']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_depth']))
                raise TypeError(msg['wrong_depth'])
            elif not self.get_planner(pln_data):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_planner_id']))
                raise TypeError(msg['wrong_planner_id'])
            elif not self.check_unit_id(planner['unit']):
                logger.warning("[{}] {}".format(pln_data.user_id,msg['wrong_unit_id']))
                raise TypeError(msg['wrong_unit_id'])

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
                    {
                        fld_pln_name: planner['name'] ,
                        fld_pln_width: float(planner['width']) ,
                        fld_pln_height: float(planner['height']) ,
                        fld_pln_depth: float(planner['depth']) ,
                        fld_pln_unit_id: ObjectId(planner['unit']) ,
                        fld_pln_latest_updated: date
                    }
                },
            )

            logger.info("[{}] Edited a planner".format(pln_data.user_id))
            result = { 'mes' : "edited_planner", 'status' : "success"}
            return result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
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
                    { 
                        fld_pln_status: item['fld_pln_REMOVE'] ,
                        fld_pln_latest_updated: date
                    }
                },
            )

            logger.info("[{}] Deleted a planner".format(pln_data.user_id))
            result = { 'mes' : "deleted_planner", 'status' : "success"}
            return result
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def is_number(self, number):
        try:
            float(number)
            int(number)
            return True
        except ValueError:
            return False
    
    def check_name_format(self, name):
        name_rex = "^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$"
        result_regex = re.search(name_rex, name)
        if((not result_regex) or len(name) < 3 or len(name) > 30):
            return False
        else:
            return True

    def check_unit_id(self,unit_id):
        for val in self.get_all_unit():
            if val['_id'] == unit_id:
                return True
        return False

    def get_all_unit(self):
        try:
            query_result = clp_unit.find()
            arr = []
            for val in query_result:
                # If there are ObjectId instances then change its value to string
                val['_id'] = str(val['_id']) 
                arr.append(val)
            return arr
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    def render_container(self, pln_data = PlannerData()):
        pass

    def __del__(self):
        client.close()
   