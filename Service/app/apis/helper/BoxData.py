# BoxData
# Description : สำหรับเก็บข้อมูลนำเข้าของ 1 กล่องบรรจุสินค้า
# Author : Athiruj Poositaporn

from .PlannerData import PlannerData

class BoxData(PlannerData):
    def __init__(self, box_id=0, boxes=None, excel_file=None):
        super().__init__()
        self.box_id = box_id 
        self.boxes = boxes
        self.excel_file = excel_file