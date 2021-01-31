# PlannerController
# Description : คลาสสำหรับ CRUD ข้อมูลของแผนการจัดเรียง (Planner)
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
from unit_converter.converter import converts
from ..box.BoxController import BoxController, BoxData
from ..packer import global_var, Packer, Box, Node
logger = logging.getLogger("planner_controller")

client = MongoClient(item["db_host"])
db = client.CLP_DB
clp_user = db[item['db_col_user']]
clp_unit = db[item['db_col_unit']]
clp_container_std = db[item['db_col_container_std']]

class PlannerController:
    # get_all_planner
    # Description : ฟังก์ชันดึงข้อมูลของ Planner ทั้งหมดตาม user_id
    # Author : Athiruj Poositaporn
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

                box_cont = BoxController()
                pln_unit = box_cont.get_unit(rs_arr[index][item['fld_pln_unit_id']])
                rs_arr[index]['pln_unit'] = pln_unit
                # Store ACTIVE planner
                arr.append(rs_arr[index])
            return arr
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # get_continer_std
    # Description : ฟังก์ชันดึงข้อมูลของ continer ขนาดมาตราฐานทั้งหมด
    # Author : Athiruj Poositaporn  
    def get_continer_std(self, pln_data = PlannerData()):
        try:
            query_result = clp_container_std.find()
            arr = []
            box_cont = BoxController()
            for val in query_result:
                val['_id'] = str(val['_id'])
                val[item['fld_con_std_unit_id']] = str(val[item['fld_con_std_unit_id']])
                val['con_std_unit'] = box_cont.get_unit(val[item['fld_con_std_unit_id']])
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

    # get_planner
    # Description : ฟังก์ชันดึงข้อมูลของ 1 Planner ตาม planner_id และ user_id
    # Author : Athiruj Poositaporn
    def get_planner(self, pln_data = PlannerData()):
        try:
            srt_fild = "{}.$".format(item['fld_user_planners'])
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
                        for index in range(len(query_result[key])):
                            query_result[key][index] = str(query_result[key][index])
                    if isinstance(query_result[key],ObjectId):
                        query_result[key] = str(query_result[key])
                box_cont = BoxController()
                pln_unit = box_cont.get_unit(query_result[item['fld_pln_unit_id']])
                query_result['pln_unit'] = pln_unit
                return query_result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # add_planner
    # Description : ฟังก์ชันเพิ่ม Planner ให้แก่ user_id
    # Author : Athiruj Poositaporn
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
            result = { 'mes' : "Added a planner successfully", 'status' : "success"}
            return result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
    
    # edit_planner
    # Description : ฟังก์ชันแก้ไข 1 Planner ตาม planner_id และ user_id
    # Author : Athiruj Poositaporn
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
            result = { 'mes' : "Edited a planner successfully", 'status' : "success"}
            return result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result
        
    # delete_planner
    # Description : ฟังก์ชันเปลี่ยนสถานะของ 1 Planner ให้เป็น REMOVE ตาม planner_id และ user_id
    # Author : Athiruj Poositaporn
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
            result = { 'mes' : "Deleted a planner successfully", 'status' : "success"}
            return result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # is_number
    # Description : ฟังก์ชันตรวจสอบข้อมูลนำเข้าเป็นตัวเลขหรือไม่
    # Author : Athiruj Poositaporn
    def is_number(self, number):
        try:
            float(number)
            # int(number)
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
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # render_container
    # Description : ฟังก์ชันประมวลผลการจัดเรียงกล่องบรรจุสินค้าในตู้บรรทุกสินค้า
    # Author : Athiruj Poositaporn     
    def render_container(self, pln_data = PlannerData()):
        try:
            # Prepare boxes data
            box_data = BoxData()
            box_data.planner_id = pln_data.planner_id
            box_data.user_id = pln_data.user_id
            box_cont = BoxController()
            arr_boxes = box_cont.get_all_box(box_data)

            global_var.init()
            # Init global variables
            
            # Create packer
            box_packer = Packer.Packer()
            
            # Prepare planner data
            planner = self.get_planner(pln_data)
            planner_width = planner[item['fld_pln_width']]
            planner_height = planner[item['fld_pln_height']]
            planner_depth = planner[item['fld_pln_depth']]
            planner_unit = planner['pln_unit']

            # Add container dimension
            box_packer.add_root_node(Node.Node(planner_width, planner_height, planner_depth))

            # Loop for add boxes to packer
            for box in arr_boxes:
                qty = box[item['fld_box_quantity']]
                for number in range(qty):
                    box_unit = box['box_unit']
                    # box_width = self.unit_converter(box[item['fld_box_width']], box_unit, planner_unit)
                    box_depth = self.unit_converter(box[item['fld_box_width']], box_unit, planner_unit)
                    box_height = self.unit_converter(box[item['fld_box_height']], box_unit, planner_unit)
                    box_width = self.unit_converter(box[item['fld_box_depth']], box_unit, planner_unit)
                    # box_depth = self.unit_converter(box[item['fld_box_depth']], box_unit, planner_unit)
                    new_box = Box.Box()
                    new_box.id = str(box['_id'])
                    new_box.name = "{}-{}".format(box[item['fld_box_name']], number+1)
                    new_box.width = box_width
                    new_box.height = box_height
                    new_box.depth = box_depth
                    new_box.unit = planner_unit
                    new_box.color = box['box_color']

                    box_packer.add_box(new_box)
            
            # Pack all boxes
            box_packer.pack()
            

            # Get boxes all result
            # arr_stack = {}
            arr_stack = []
            logger.info("len(global_var.UNFITTED_ITEMS) : {}".format(len(global_var.UNFITTED_ITEMS)))
            global_var.BASE_BOXES.sort(key=lambda x: (x.position[2]), reverse=False)
            for index in range(len(global_var.BASE_BOXES)):
                box_packer.get_stack(root = global_var.BASE_BOXES[index], opt = False)
                # arr_stack['stack_{}'.format(index)] = global_var.BOXES_STACK_DETAIL
                arr_stack.append(global_var.BOXES_STACK_DETAIL)
                global_var.BOXES_STACK_DETAIL = []
            
            total_volume = global_var.USED_VOLUME / box_packer.root_nodes[0].get_volume() * 100
            total_volume = round(total_volume, 4)
            container_detail = {
                'total_volume' : total_volume,
                'unfit_boxes' : box_packer.format_unfitted_item(),
                # 'unfit_boxes' : global_var.UNFITTED_ITEMS,
            }
            result = {
                'container_detail' : container_detail,
                'boxes_stack' : arr_stack,
            }
            return result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # unit_converter
    # Description : ฟังก์ชันแปลงหน่วยความยาว
    # Author : Athiruj Poositaporn   
    def unit_converter(self,number, old_unit, new_unit):
        try:
            if old_unit == new_unit:
                return number
            if(new_unit == 'in'):
                new_unit = 'inch'
            if(old_unit == 'in'):
                old_unit = 'inch'
            old_num = '{} {}'.format(number,old_unit)
            num = converts(old_num , new_unit)
            return round(float(num), 2)
        except Exception as identifier:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def __del__(self):
        client.close()
   