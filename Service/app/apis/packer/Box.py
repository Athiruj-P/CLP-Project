# Box
# Description : คลาสจัดการข้อมูลภายใน Box
# Author : Athiruj Poositaporn

import logging
import logging.config
from .RotationType import RotationType
logger = logging.getLogger("planner_controller")

class Box:
    def __init__(self):
        self.name = ""
        self.width = 0
        self.height = 0
        self.depth = 0
        self.unit = ""
        self.color = ""
        self.rotation_type = 0
        self.fixed_direction = False

    # get_volume
    # Description : ฟังก์ชันคำนวณปริมาตรของ Box
    # Author : Athiruj Poositaporn
    def get_volume(self):
        return self.width * self.height * self.depth

    # get_int_dimension
    # Description : ฟังก์ชันคือค่าขนาดของ Box ในรูปแบบ Int
    # Author : Athiruj Poositaporn  
    def get_int_dimension(self):
        dim = self.get_dimension()
        return int(dim[0]),int(dim[1]),int(dim[2])

    # get_int_dimension
    # Description : ฟังก์ชันคือค่าข้อมูลของ Box
    # Author : Athiruj Poositaporn
    def get_detail(self):
        return {
            'box_name' : self.name,
            'box_width' : self.width,
            'box_height' : self.height,
            'box_depth' : self.depth,
            'box_unit' : self.unit,
            'box_color' : self.color,
        }

    # get_dimension
    # Description : ฟังก์ชันคือค่าขนาดของ Box ตามทิศทางการหมุน (rotation_type)
    # Author : Athiruj Poositaporn   
    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
        else:
            dimension = []

        return dimension