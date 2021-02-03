# ExcelController
# Description : คลาสสำหรับจัดการข้อมูลของกล่องบรรจุสินค้าจากไฟล์ Excel
# Author : Athiruj Poositaporn

import pandas as pd
from .BoxController import BoxController, BoxData, item, msg, Date, ObjectId
import logging
import logging.config

logger = logging.getLogger("excel_controller")


class ExcelController(BoxController):
    def __init__(self):
        self.COLUMNS = ['name', 'width', 'height', 'depth', 'qty', 'unit']
        self.NAME = 0
        self.WIDTH = 1
        self.HEIGHT = 2
        self.DEPTH = 3
        self.QTY = 4
        self.UNIT = 5

    # ExcelController
    # Description : ฟังก์ชันดึงข้อมูลของกล่องบรรจุสินค้าจากไฟล์ Excel
    # Author : Athiruj Poositaporn
    def get_excel_box(self, data=BoxData()):
        try:
            df = pd.read_excel(data.excel_file)
            # Check columns name
            for col in df.columns:
                if col not in self.COLUMNS:
                    logger.warning("[{}] {}".format(
                        data.user_id, msg['wrong_column_name']))
                    raise TypeError(msg['wrong_column_name'])

            # Check box's name
            for row in df[self.COLUMNS[self.NAME]]:
                if not self.check_name_format(row):
                    logger.warning("[{}] {}".format(
                        data.user_id, msg['wrong_name_format']))
                    raise TypeError(msg['wrong_name_format'])

            # Check box's unit
            arr_unit = self.get_all_unit()
            arr_abb = []
            arr_id = []
            # get unit abbreviation
            for val in arr_unit:
                arr_id.append(val['_id'])
                arr_abb.append(val[item['fld_un_abb']])

            for index in range(len(df[self.COLUMNS[self.UNIT]])):
                try:
                    row = df[self.COLUMNS[self.UNIT]][index]
                    unit_index = arr_abb.index(row.lower())
                    df[self.COLUMNS[self.UNIT]].at[index] = arr_id[unit_index]
                except Exception as identifier:
                    logger.warning("[{}] {}".format(
                        data.user_id, msg['wrong_unit_abb']))
                    raise TypeError(msg['wrong_unit_abb'])

            # Check box's width
            for row in df[self.COLUMNS[self.WIDTH]]:
                if not self.is_number(row):
                    logger.warning("[{}] {}".format(
                        data.user_id, msg['wrong_width']))
                    raise TypeError(msg['wrong_width'])

            # Check box's height
            for row in df[self.COLUMNS[self.HEIGHT]]:
                if not self.is_number(row):
                    logger.warning("[{}] {}".format(
                        data.user_id, msg['wrong_height']))
                    raise TypeError(msg['wrong_height'])

            # Check box's depth
            for row in df[self.COLUMNS[self.DEPTH]]:
                if not self.is_number(row):
                    logger.warning("[{}] {}".format(
                        data.user_id, msg['wrong_depth']))
                    raise TypeError(msg['wrong_depth'])

            # Check box's quantity
            for row in df[self.COLUMNS[self.QTY]]:
                if not self.is_number(row):
                    logger.warning("[{}] {}".format(
                        data.user_id, msg['wrong_qty']))
                    raise TypeError(msg['wrong_qty'])

            # get colors
            arr_color = self.get_all_color()

            # Re-format data
            arr_result = []
            for index, row in df.iterrows():
                unit_index = arr_id.index(row['unit'])
                tmp_unit = arr_abb[unit_index]
                tmp_rs_width = self.check_lenght(
                    float(row['width']), tmp_unit)
                tmp_rs_height = self.check_lenght(
                    float(row['height']), tmp_unit)
                tmp_rs_depth = self.check_lenght(
                    float(row['depth']), tmp_unit)
                tmp_rs_qty = self.check_quantity(int(row['qty']))

                if(not tmp_rs_width['status']):
                    raise TypeError(tmp_rs_width['mes'])
                elif(not tmp_rs_height['status']):
                    raise TypeError(tmp_rs_height['mes'])
                elif(not tmp_rs_depth['status']):
                    raise TypeError(tmp_rs_depth['mes'])
                elif(not tmp_rs_qty):
                    raise TypeError(msg['wrong_qty_size'])

                date = Date.get_datetime_now()
                color_id = arr_color[index % len(arr_color)]['_id']
                arr_result.append({
                    "_id": ObjectId(),
                    item["fld_box_name"]: row['name'],
                    item["fld_box_width"]: float(row['width']),
                    item["fld_box_height"]: float(row['height']),
                    item["fld_box_depth"]: float(row['depth']),
                    item["fld_box_quantity"]: int(row['qty']),
                    item["fld_box_unit_id"]: row['unit'],
                    item["fld_box_color_id"]: color_id,
                    item["fld_box_created_date"]: date,
                    item["fld_box_latest_updated"]: date,
                    item["fld_box_status"]: item["fld_box_ACTIVE"],
                })
            return {'status': 'success', 'data': arr_result}
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(str(identifier))]
                result = {'mes': str(identifier), 'status': "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes': "Wrong data format.",
                          'status': "system_error"}
            return result

    # check_lenght
    # Description : ฟังก์ชันตรวจสอบความยาวของกล่อง
    # Author : Athiruj Poositaporn
    def check_lenght(self, number, unit):
        cm_lower = 1
        cm_upper = 1500
        in_lower = 0.39
        in_upper = 590
        str_num = str(number)

        lower = cm_lower
        upper = cm_upper
        err_mes = msg['wrong_lenght_cm']

        if (unit == "inch" or unit == "in"):
            lower = in_lower
            upper = in_upper
            err_mes = msg['wrong_lenght_in']

        if(number < lower or number > upper):
            return {'status': False, 'mes': err_mes}
        elif (len(str_num.split('.')[1]) > 4):
            return {'status': False, 'mes': msg['wrong_decimal']}
        else:
            return {'status': True}

    # check_quantity
    # Description : ฟังก์ชันตรวจสอบจำนวนของกล่อง
    # Author : Athiruj Poositaporn
    def check_quantity(self, qty):
        return qty >= 1 and qty <= 100
