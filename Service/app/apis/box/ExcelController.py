import pandas as pd
from .BoxController import BoxController

logger = logging.getLogger("excel_controller")

client = MongoClient(item["db_host"])
db = client.CLP_DB
clp_user = db[item['db_col_user']]
clp_unit = db[item['db_col_unit']]
clp_box_std = db[item['db_col_box_std']]
clp_color = db[item['db_col_color']]
clp_box = db[item['db_col_box']]

class ExcelController(BoxController):
    def __init__(self):
        self.COLUMNS = ['name', 'width', 'height', 'depth', 'qty', 'unit']

    def get_excel_box(self, file):
        try:
            df = pd.read_excel(file)
            arr = []
            for index, row in df.iterrows():
                arr.append({
                    'name' : row['name'],
                    'width' : row['width'],
                    'height' : row['height'],
                    'depth' : row['depth'],
                    'qty' : row['qty'],
                    'unit' : row['unit'],
                })
        except Exception as identifier:
            try:
                list(msg.keys())[list(msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                logger.error("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result