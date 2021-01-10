import pandas as pd
from .BoxController import BoxController, BoxData , item, msg, Date, ObjectId
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

    def get_excel_box(self, data = BoxData()):
        try:
            df = pd.read_excel(data.excel_file)
            # Check columns name
            for col in df.columns:
                if col not in self.COLUMNS:
                    logger.warning("[{}] {}".format(data.user_id,msg['wrong_column_name']))
                    raise TypeError(msg['wrong_column_name'])
            
            # Check box's name            
            for row in df[self.COLUMNS[self.NAME]]:
                if not self.check_name_format(row):
                    logger.warning("[{}] {}".format(data.user_id,msg['wrong_name_format']))
                    raise TypeError(msg['wrong_name_format'])
            
            # Check box's width            
            for row in df[self.COLUMNS[self.WIDTH]]:
                if not self.is_number(row):
                    logger.warning("[{}] {}".format(data.user_id,msg['wrong_width']))
                    raise TypeError(msg['wrong_width'])
            
            # Check box's height            
            for row in df[self.COLUMNS[self.HEIGHT]]:
                if not self.is_number(row):
                    logger.warning("[{}] {}".format(data.user_id,msg['wrong_height']))
                    raise TypeError(msg['wrong_height'])
            
            # Check box's depth            
            for row in df[self.COLUMNS[self.DEPTH]]:
                if not self.is_number(row):
                    logger.warning("[{}] {}".format(data.user_id,msg['wrong_depth']))
                    raise TypeError(msg['wrong_depth'])
            
            # Check box's quantity            
            for row in df[self.COLUMNS[self.QTY]]:
                if not self.is_number(row):
                    logger.warning("[{}] {}".format(data.user_id,msg['wrong_qty']))
                    raise TypeError(msg['wrong_qty'])
            
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
                    logger.warning("[{}] {}".format(data.user_id,msg['wrong_unit_abb']))
                    raise TypeError(msg['wrong_unit_abb'])
            
            # get colors
            arr_color = self.get_all_color()

            # Re-format data
            arr_result = []
            for index, row in df.iterrows():
                date = Date.get_datetime_now()
                color_id = arr_color[index % len(arr_color)]['_id']
                arr_result.append({
                    "_id" : ObjectId(),
                    item["fld_box_name"] : row['name'],
                    item["fld_box_width"] : float( row['width']),
                    item["fld_box_height"] : float( row['height']),
                    item["fld_box_depth"] : float( row['depth']),
                    item["fld_box_quantity"] : int( row['qty']),
                    item["fld_box_unit_id"] : row['unit'],
                    item["fld_box_color_id"] : color_id,
                    item["fld_box_created_date"] : date,
                    item["fld_box_latest_updated"] : date,
                    item["fld_box_status"] : item["fld_box_ACTIVE"],
                })
            return arr_result
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result