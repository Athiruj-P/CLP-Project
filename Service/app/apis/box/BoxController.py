# BoxController
# Description : คลาสสำหรับ CRUD ข้อมูลของกล่องบรรจุสินค้า (ฺBox)
# Author : Athiruj Poositaporn

from flask import jsonify
import datetime, pytz
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid  import ObjectId
import logging
import logging.config
from ..db_config import item
from ..helper.BoxData import BoxData
from ..helper import Date
from ..err_msg import msg
import re

logger = logging.getLogger("box_controller")

client = MongoClient(item["db_host"])
db = client.CLP_DB
clp_user = db[item['db_col_user']]
clp_unit = db[item['db_col_unit']]
clp_box_std = db[item['db_col_box_std']]
clp_color = db[item['db_col_color']]
clp_box = db[item['db_col_box']]

class BoxController:
    # get_box_std
    # Description : ฟังก์ชันดึงข้อมูลของ Box ขนาดมาตราฐานทั้งหมด
    # Author : Athiruj Poositaporn  
    def get_box_std(self, box_data = BoxData()):
        try:
            query_result = clp_box_std.find()
            arr = []
            # Loop to change ObjectId to string
            for val in query_result:
                val['_id'] = str(val['_id'])
                val[item['fld_box_std_unit_id']] = str(val[item['fld_box_std_unit_id']])
                val['box_std_unit'] = self.get_unit(val[item['fld_box_std_unit_id']])
                arr.append(val)
            return arr
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # get_all_box
    # Description : ฟังก์ชันดึงข้อมูลของ Box ทั้งหมดตาม planner_id
    # Author : Athiruj Poositaporn 
    def get_all_box(self, box_data = BoxData()):
        try:
            srt_fild = "{}.$".format(item['fld_user_planners'])
            query_result = clp_user.find_one(
                {
                    item['fld_user_planners']:{
                        '$elemMatch': {"_id" : ObjectId(box_data.planner_id) }
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
                pln_boxes = query_result[item['fld_pln_boxes']]
                arr = []
                for box_id in pln_boxes:
                    query_box_detail = clp_box.find_one(
                        { '_id' : box_id}
                    )
                    if query_box_detail[item['fld_box_status']] == item['fld_box_REMOVE']:
                        continue
                    query_box_detail['_id'] = str(query_box_detail['_id'])
                    unit_id = str(query_box_detail[item['fld_box_unit_id']])
                    color_id = str(query_box_detail[item['fld_box_color_id']])
                    query_box_detail[item['fld_box_unit_id']] = unit_id
                    query_box_detail[item['fld_box_color_id']] = color_id
                    query_box_detail['box_unit'] = self.get_unit(unit_id)
                    query_box_detail['box_color'] = self.get_color(color_id)
                    arr.append(query_box_detail)
                
                return arr
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    # add_box
    # Description : ฟังก์ชันเพิ่มข้อมูลของ 1 Box ให้แก่ planner_id และ user_id
    # Author : Athiruj Poositaporn 
    def add_box(self, box_data = BoxData()):
        try:
            logger.info("[{}] Prepair Boxes data to be save".format(box_data.user_id))
            boxes = box_data.boxes
            # Validation
            if not self.check_name_format(boxes['name']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_name_format']))
                raise TypeError(msg['wrong_name_format'])

            elif not self.is_number(boxes['width']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_width']))
                raise TypeError(msg['wrong_width'])

            elif not self.is_number(boxes['height']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_height']))
                raise TypeError(msg['wrong_height'])

            elif not self.is_number(boxes['depth']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_depth']))
                raise TypeError(msg['wrong_depth'])

            elif not self.is_number(boxes['qty']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_qty']))
                raise TypeError(msg['wrong_qty'])

            elif not self.check_unit_id(boxes['unit']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_unit_id']))
                raise TypeError(msg['wrong_unit_id'])

            elif not self.check_color_id(boxes['color']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_color_id']))
                raise TypeError(msg['wrong_color_id'])
            
            date = Date.get_datetime_now()
            new_boxes_id = ObjectId()
            new_boxes = {
                   "_id" : new_boxes_id,
                   item["fld_box_name"] : boxes['name'],
                   item["fld_box_width"] :float( boxes['width']),
                   item["fld_box_height"] :float( boxes['height']),
                   item["fld_box_depth"] :float( boxes['depth']),
                   item["fld_box_quantity"] :int( boxes['qty']),
                   item["fld_box_unit_id"] : ObjectId(boxes['unit']),
                   item["fld_box_color_id"] : ObjectId(boxes['color']),
                   item["fld_box_created_date"] : date,
                   item["fld_box_latest_updated"] : date,
                   item["fld_box_status"] : item["fld_box_ACTIVE"],
            }

            fld_user_pln = "{}._id".format(item["fld_user_planners"])
            fld_pln_box = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_boxes'])

            clp_box.insert_one(new_boxes)
            clp_user.update(
                {
                    '_id': ObjectId(box_data.user_id),
                    fld_user_pln : ObjectId(box_data.planner_id),
                },
                { '$push': {fld_pln_box : new_boxes_id} }
            )


            logger.info("[{}] Added boxes to planner".format(box_data.user_id))
            result = { 'mes' : "Added boxes successfully", 'status' : "success"}
            return result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # add_box_by_excel
    # Description : ฟังก์ชันเพิ่มข้อมูลของ Box จากไฟล์ Excel ให้แก่ planner_id และ user_id
    # Author : Athiruj Poositaporn 
    def add_box_by_excel(self, box_data = BoxData()):
        try:
            fld_user_pln = "{}._id".format(item["fld_user_planners"])
            fld_pln_box = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_boxes'])
            
            for box in box_data.boxes:
                new_boxes_id = box['_id']
                clp_box.insert_one(box)
                clp_user.update(
                    {
                        '_id': ObjectId(box_data.user_id),
                        fld_user_pln : ObjectId(box_data.planner_id),
                    },
                    { '$push': {fld_pln_box : new_boxes_id} }
                )


            logger.info("[{}] Added boxes from an excel to planner".format(box_data.user_id))
            result = { 'mes' : "Added boxes from excel successfully", 'status' : "success"}
            return result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # edit_box
    # Description : ฟังก์ชันแก้ไขข้อมูลของ 1 Box ตาม planner_id และ user_id
    # Author : Athiruj Poositaporn 
    def edit_box(self, box_data = BoxData()):
        try:
            logger.info("[{}] Prepair Boxes data to be save".format(box_data.user_id))
            boxes = box_data.boxes
            # Validation
            if not self.check_name_format(boxes['name']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_name_format']))
                raise TypeError(msg['wrong_name_format'])

            elif not self.is_number(boxes['width']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_width']))
                raise TypeError(msg['wrong_width'])

            elif not self.is_number(boxes['height']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_height']))
                raise TypeError(msg['wrong_height'])

            elif not self.is_number(boxes['depth']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_depth']))
                raise TypeError(msg['wrong_depth'])

            elif not self.is_number(boxes['qty']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_qty']))
                raise TypeError(msg['wrong_qty'])

            elif not self.check_unit_id(boxes['unit']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_unit_id']))
                raise TypeError(msg['wrong_unit_id'])

            elif not self.check_color_id(boxes['color']):
                logger.warning("[{}] {}".format(box_data.user_id,msg['wrong_color_id']))
                raise TypeError(msg['wrong_color_id'])
            
            date = Date.get_datetime_now()
            new_boxes_id = ObjectId()
            new_boxes = {
                   "_id" : new_boxes_id,
                   item["fld_box_name"] : boxes['name'],
                   item["fld_box_width"] :float( boxes['width']),
                   item["fld_box_height"] :float( boxes['height']),
                   item["fld_box_depth"] :float( boxes['depth']),
                   item["fld_box_quantity"] :int( boxes['qty']),
                   item["fld_box_unit_id"] : ObjectId(boxes['unit']),
                   item["fld_box_color_id"] : ObjectId(boxes['color']),
            }

            fld_user_pln = "{}._id".format(item["fld_user_planners"])
            fld_pln_box = "{}.$.{}".format(item['fld_user_planners'], item['fld_pln_boxes'])

            clp_box.update(
                {'_id': ObjectId(box_data.box_id)},
                {
                    '$set' : 
                    { 
                        item["fld_box_name"] : boxes['name'],
                        item["fld_box_width"] :float( boxes['width']),
                        item["fld_box_height"] :float( boxes['height']),
                        item["fld_box_depth"] :float( boxes['depth']),
                        item["fld_box_quantity"] :int( boxes['qty']),
                        item["fld_box_unit_id"] : ObjectId(boxes['unit']),
                        item["fld_box_color_id"] : ObjectId(boxes['color']),
                        item['fld_box_latest_updated'] : date
                    }
                },
            )

            logger.info("[{}] Edited a box planner".format(box_data.user_id))
            result = { 'mes' : "Edited boxes successfully", 'status' : "success"}
            return result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # delete_box
    # Description : ฟังก์ชันเปลี่ยนสถานะของ 1 Box เป็น "REMOVE" ตาม box_id
    # Author : Athiruj Poositaporn 
    def delete_box(self, box_data = BoxData()):
        try:
            date = Date.get_datetime_now()
            
            clp_box.update(
                {'_id': ObjectId(box_data.box_id)},
                {
                    '$set' : 
                    { 
                        item['fld_box_status'] : item['fld_box_REMOVE'] ,
                        item['fld_box_latest_updated'] : date
                    }
                },
            )

            logger.info("[{}] Deleted boxes".format(box_data.user_id))
            result = { 'mes' : "Deleted boxes successfully", 'status' : "success"}
            return result
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # is_number
    # Description : ฟังก์ชันตรวจสอบข้อมูลนำเข้าเป็นตัวเลขหรือไม่
    # Author : Athiruj Poositaporn
    def is_number(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    # check_name_format
    # Description : ฟังก์ชันตรวจสอบชื่อของ Planner ว่าตรงตามรูปแบบที่กำหนดหรือไม่
    # Author : Athiruj Poositaporn   
    def check_name_format(self, name):
        name_rex = "^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$"
        result_regex = re.search(name_rex, name)
        if((not result_regex) or len(name) < 3 or len(name) > 30):
            return False
        else:
            return True

    # check_unit_id
    # Description : ฟังก์ชันตรวจสอบ unit_id มีจริงหรือไม่
    # Author : Athiruj Poositaporn 
    def check_unit_id(self,unit_id):
        for val in self.get_all_unit():
            if val['_id'] == unit_id:
                return True
        return False

    # check_color_id
    # Description : ฟังก์ชันตรวจสอบ color_id มีจริงหรือไม่
    # Author : Athiruj Poositaporn 
    def check_color_id(self,color_id):
        for val in self.get_all_color():
            if val['_id'] == color_id:
                return True
        return False

    # get_all_unit
    # Description : ฟังก์ชันดึงข้อมูลของหน่วยความยาวทั้งหมด
    # Author : Athiruj Poositaporn  
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

    # get_unit
    # Description : ฟังก์ชันดึงข้อมูลของหน่วยความยาวตาม unit_id
    # Author : Athiruj Poositaporn 
    def get_unit(self, unit_id):
        try:
            query_result = clp_unit.find_one(
                {'_id' : ObjectId(unit_id)}
            )
            return query_result[item['fld_un_abb']]
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # get_all_color
    # Description : ฟังก์ชันดึงข้อมูลสีทั้งหมด
    # Author : Athiruj Poositaporn
    def get_all_color(self):
        try:
            query_result = clp_color.find()
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
    
    # get_color
    # Description : ฟังก์ชันดึงข้อมูลของสีตาม color_id
    # Author : Athiruj Poositaporn 
    def get_color(self, color_id):
        try:
            query_result = clp_color.find_one(
                {'_id' : ObjectId(color_id)}
            )
            return query_result[item['fld_color_hex']]
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def __del__(self):
        client.close()
   